#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use eframe::egui;
use rfd::FileDialog;
use std::collections::BTreeMap;
use std::env;
use std::fs;
use std::io;
use std::path::{Path, PathBuf};

const ANCHOR_DIR: &str = ".tharness";
const MANIFEST_NAME: &str = "project.yaml";
const AGENTS_NAME: &str = "AGENTS.md";
const AGENTS_BLOCK_START: &str = "<!-- THARNESS_BINDING_START -->";
const AGENTS_BLOCK_END: &str = "<!-- THARNESS_BINDING_END -->";

fn main() -> eframe::Result<()> {
    let native_options = eframe::NativeOptions {
        viewport: egui::ViewportBuilder::default()
            .with_inner_size([780.0, 560.0])
            .with_min_inner_size([700.0, 500.0]),
        ..Default::default()
    };

    eframe::run_native(
        "THarness 绑定工具",
        native_options,
        Box::new(|cc| {
            configure_fonts(&cc.egui_ctx);
            configure_style(&cc.egui_ctx);
            Box::new(BinderApp::new())
        }),
    )
}

#[derive(Clone, Copy, PartialEq, Eq)]
enum OverwriteChoice {
    None,
    Waiting,
}

struct BinderApp {
    tharness_root: PathBuf,
    target_root: Option<PathBuf>,
    status: StatusMessage,
    overwrite_choice: OverwriteChoice,
}

#[derive(Clone)]
struct StatusMessage {
    text: String,
    kind: StatusKind,
}

#[derive(Clone, Copy)]
enum StatusKind {
    Ready,
    Success,
    Warning,
    Error,
}

impl StatusMessage {
    fn ready(text: impl Into<String>) -> Self {
        Self {
            text: text.into(),
            kind: StatusKind::Ready,
        }
    }

    fn success(text: impl Into<String>) -> Self {
        Self {
            text: text.into(),
            kind: StatusKind::Success,
        }
    }

    fn warning(text: impl Into<String>) -> Self {
        Self {
            text: text.into(),
            kind: StatusKind::Warning,
        }
    }

    fn error(text: impl Into<String>) -> Self {
        Self {
            text: text.into(),
            kind: StatusKind::Error,
        }
    }

    fn color(&self) -> egui::Color32 {
        match self.kind {
            StatusKind::Ready => egui::Color32::from_rgb(184, 194, 211),
            StatusKind::Success => egui::Color32::from_rgb(70, 211, 137),
            StatusKind::Warning => egui::Color32::from_rgb(245, 178, 81),
            StatusKind::Error => egui::Color32::from_rgb(255, 107, 107),
        }
    }
}

impl BinderApp {
    fn new() -> Self {
        let tharness_root = resolve_tharness_root();
        let status = if validate_tharness_root(&tharness_root) {
            StatusMessage::ready("准备就绪")
        } else {
            StatusMessage::error("THarness 主工程无效，请从主目录的 THarness-Binder.exe 启动。")
        };

        Self {
            tharness_root,
            target_root: None,
            status,
            overwrite_choice: OverwriteChoice::None,
        }
    }

    fn can_bind(&self) -> bool {
        validate_tharness_root(&self.tharness_root) && self.target_root.is_some()
    }

    fn bind(&mut self, force: bool) {
        self.overwrite_choice = OverwriteChoice::None;
        let Some(target_root) = self.target_root.clone() else {
            self.status = StatusMessage::warning("请先选择目标项目文件夹。");
            return;
        };

        match bind_project(&self.tharness_root, &target_root, force) {
            Ok(BindOutcome::Written) => {
                self.status = StatusMessage::success("绑定完成。");
            }
            Ok(BindOutcome::Unchanged) => {
                self.status = StatusMessage::success("绑定已是最新。");
            }
            Err(BindError::WouldOverwrite(path)) => {
                self.status = StatusMessage::warning(format!(
                    "目标锚点已有本地修改，需要确认覆盖：{}",
                    path.display()
                ));
                self.overwrite_choice = OverwriteChoice::Waiting;
            }
            Err(BindError::Io(err)) => {
                self.status = StatusMessage::error(format!("绑定失败：{err}"));
            }
        }
    }
}

impl eframe::App for BinderApp {
    fn update(&mut self, ctx: &egui::Context, _frame: &mut eframe::Frame) {
        egui::CentralPanel::default()
            .frame(egui::Frame::none().fill(app_bg()))
            .show(ctx, |ui| {
                ui.add_space(18.0);
                ui.vertical_centered(|ui| {
                    ui.label(
                        egui::RichText::new("THarness 绑定工具")
                            .heading()
                            .strong()
                            .size(28.0)
                            .color(primary_text()),
                    );
                    ui.add_space(4.0);
                    ui.label(
                        egui::RichText::new("把当前 THarness 主工程绑定到指定项目目录")
                            .strong()
                            .size(17.0)
                            .color(secondary_text()),
                    );
                });

                ui.add_space(20.0);
                panel(ui, |ui| {
                    section_label(ui, "THarness 主工程");
                    let mut tharness_root_text = self.tharness_root.display().to_string();
                    readonly_field(ui, &mut tharness_root_text, "");
                    let root_status = if validate_tharness_root(&self.tharness_root) {
                        egui::RichText::new("状态：主工程有效")
                            .strong()
                            .color(StatusMessage::success("").color())
                    } else {
                        egui::RichText::new("状态：主工程无效")
                            .strong()
                            .color(StatusMessage::error("").color())
                    };
                    ui.add_space(6.0);
                    ui.label(root_status);
                });

                ui.add_space(14.0);
                panel(ui, |ui| {
                    section_label(ui, "目标项目文件夹");
                    ui.horizontal(|ui| {
                        let button_size = egui::vec2(132.0, 42.0);
                        let field_width = (ui.available_width() - button_size.x - 12.0).max(280.0);
                        let mut target_text = self
                            .target_root
                            .as_ref()
                            .map(|path| path.display().to_string())
                            .unwrap_or_default();
                        readonly_field_sized(
                            ui,
                            &mut target_text,
                            "请选择需要绑定的项目目录",
                            field_width,
                        );
                        ui.add_space(12.0);
                        if flat_button_sized(ui, "选择文件夹", button_size).clicked() {
                            if let Some(folder) = FileDialog::new().pick_folder() {
                                self.target_root = Some(folder);
                                self.overwrite_choice = OverwriteChoice::None;
                                self.status = StatusMessage::ready("准备就绪");
                            }
                        }
                    });
                });

                ui.add_space(14.0);
                panel(ui, |ui| {
                    section_label(ui, "绑定预览");
                    if let Some(target_root) = &self.target_root {
                        ui.label(
                            egui::RichText::new(format!(
                                "将创建：{}",
                                anchor_dir(target_root).display()
                            ))
                            .strong()
                            .color(primary_text()),
                        );
                        ui.add_space(8.0);
                        preview_box(ui, MANIFEST_NAME, "start.ps1", "start.cmd", "README.md");
                        ui.add_space(8.0);
                        ui.label(
                            egui::RichText::new(format!(
                                "并更新项目根目录：{}",
                                target_root.join(AGENTS_NAME).display()
                            ))
                            .strong()
                            .color(secondary_text()),
                        );
                    } else {
                        ui.label(
                            egui::RichText::new("选择目标文件夹后，这里会显示即将生成的绑定文件。")
                                .strong()
                                .color(secondary_text()),
                        );
                    }
                });

                ui.add_space(14.0);
                panel(ui, |ui| {
                    section_label(ui, "写入规则");
                    ui.label(
                        egui::RichText::new(
                            "通用框架、角色、规则、wiki、能力索引和工具改动写回 THarness。",
                        )
                        .strong()
                        .color(primary_text()),
                    );
                    ui.label(
                        egui::RichText::new(
                            "项目事实、项目代码、项目资源和项目专属决策留在目标项目。",
                        )
                        .strong()
                        .color(primary_text()),
                    );
                });

                ui.add_space(16.0);
                ui.horizontal(|ui| {
                    let bind_button = ui.add_enabled(self.can_bind(), primary_button("确认绑定"));
                    if bind_button.clicked() {
                        self.bind(false);
                    }

                    if self.overwrite_choice == OverwriteChoice::Waiting
                        && danger_button(ui, "覆盖已有锚点").clicked()
                    {
                        self.bind(true);
                    }

                    if flat_button(ui, "关闭").clicked() {
                        ctx.send_viewport_cmd(egui::ViewportCommand::Close);
                    }
                });
                ui.add_space(8.0);
                ui.label(
                    egui::RichText::new(format!("状态：{}", self.status.text))
                        .strong()
                        .size(16.5)
                        .color(self.status.color()),
                );
            });
    }
}

fn section_label(ui: &mut egui::Ui, text: &str) {
    ui.label(
        egui::RichText::new(text)
            .strong()
            .size(18.0)
            .color(primary_text()),
    );
}

fn configure_fonts(ctx: &egui::Context) {
    let mut fonts = egui::FontDefinitions::default();
    if let Some((name, bytes)) = load_preferred_cjk_font() {
        fonts
            .font_data
            .insert(name.clone(), egui::FontData::from_owned(bytes));
        fonts
            .families
            .entry(egui::FontFamily::Proportional)
            .or_default()
            .insert(0, name.clone());
        fonts
            .families
            .entry(egui::FontFamily::Monospace)
            .or_default()
            .insert(0, name);
    }
    ctx.set_fonts(fonts);
}

fn load_preferred_cjk_font() -> Option<(String, Vec<u8>)> {
    let candidates = [
        "C:\\Windows\\Fonts\\msyh.ttc",
        "C:\\Windows\\Fonts\\msyhbd.ttc",
        "C:\\Windows\\Fonts\\simhei.ttf",
        "C:\\Windows\\Fonts\\simsun.ttc",
    ];
    for path in candidates {
        if let Ok(bytes) = fs::read(path) {
            return Some(("tharness-cjk".to_owned(), bytes));
        }
    }
    None
}

fn configure_style(ctx: &egui::Context) {
    let mut style = (*ctx.style()).clone();
    style.spacing.item_spacing = egui::vec2(10.0, 10.0);
    style.spacing.button_padding = egui::vec2(18.0, 10.0);
    style.spacing.interact_size = egui::vec2(92.0, 40.0);
    style.text_styles = BTreeMap::from([
        (egui::TextStyle::Heading, egui::FontId::proportional(28.0)),
        (egui::TextStyle::Body, egui::FontId::proportional(17.0)),
        (egui::TextStyle::Button, egui::FontId::proportional(17.0)),
        (egui::TextStyle::Small, egui::FontId::proportional(15.5)),
        (egui::TextStyle::Monospace, egui::FontId::monospace(16.0)),
    ]);

    let mut visuals = egui::Visuals::dark();
    visuals.panel_fill = app_bg();
    visuals.window_fill = card_bg();
    visuals.window_rounding = egui::Rounding::same(18.0);
    visuals.widgets.noninteractive.bg_fill = field_bg();
    visuals.widgets.noninteractive.fg_stroke.color = primary_text();
    visuals.widgets.inactive.bg_fill = egui::Color32::from_rgb(43, 55, 75);
    visuals.widgets.inactive.fg_stroke.color = primary_text();
    visuals.widgets.hovered.bg_fill = egui::Color32::from_rgb(55, 70, 94);
    visuals.widgets.hovered.fg_stroke.color = primary_text();
    visuals.widgets.active.bg_fill = egui::Color32::from_rgb(72, 92, 124);
    visuals.widgets.active.fg_stroke.color = primary_text();
    visuals.widgets.open.bg_fill = egui::Color32::from_rgb(55, 70, 94);
    visuals.selection.bg_fill = accent();
    visuals.override_text_color = Some(primary_text());
    style.visuals = visuals;
    ctx.set_style(style);
}

fn app_bg() -> egui::Color32 {
    egui::Color32::from_rgb(14, 18, 27)
}

fn card_bg() -> egui::Color32 {
    egui::Color32::from_rgb(25, 32, 45)
}

fn field_bg() -> egui::Color32 {
    egui::Color32::from_rgb(18, 24, 35)
}

fn primary_text() -> egui::Color32 {
    egui::Color32::from_rgb(236, 241, 248)
}

fn secondary_text() -> egui::Color32 {
    egui::Color32::from_rgb(158, 171, 191)
}

fn accent() -> egui::Color32 {
    egui::Color32::from_rgb(79, 139, 255)
}

fn panel(ui: &mut egui::Ui, add_contents: impl FnOnce(&mut egui::Ui)) {
    egui::Frame::none()
        .fill(card_bg())
        .rounding(egui::Rounding::same(18.0))
        .inner_margin(egui::Margin::symmetric(18.0, 16.0))
        .show(ui, add_contents);
}

fn readonly_field(ui: &mut egui::Ui, value: &mut String, hint: &str) {
    let width = ui.available_width().max(120.0);
    readonly_field_sized(ui, value, hint, width);
}

fn readonly_field_sized(ui: &mut egui::Ui, value: &mut String, hint: &str, width: f32) {
    egui::Frame::none()
        .fill(field_bg())
        .rounding(egui::Rounding::same(12.0))
        .inner_margin(egui::Margin::symmetric(10.0, 6.0))
        .show(ui, |ui| {
            ui.add(
                egui::TextEdit::singleline(value)
                    .hint_text(hint)
                    .text_color(primary_text())
                    .desired_width(width)
                    .interactive(false)
                    .frame(false),
            );
        });
}

fn preview_box(ui: &mut egui::Ui, first: &str, second: &str, third: &str, fourth: &str) {
    egui::Frame::none()
        .fill(field_bg())
        .rounding(egui::Rounding::same(12.0))
        .inner_margin(egui::Margin::symmetric(14.0, 12.0))
        .show(ui, |ui| {
            ui.monospace(format!("{first}\n{second}\n{third}\n{fourth}"));
        });
}

fn primary_button(text: &str) -> egui::Button<'_> {
    egui::Button::new(
        egui::RichText::new(text)
            .strong()
            .size(17.0)
            .color(egui::Color32::WHITE),
    )
    .fill(accent())
    .rounding(egui::Rounding::same(14.0))
}

fn flat_button_widget(text: &str) -> egui::Button<'_> {
    egui::Button::new(
        egui::RichText::new(text)
            .strong()
            .size(17.0)
            .color(primary_text()),
    )
    .fill(egui::Color32::from_rgb(43, 55, 75))
    .rounding(egui::Rounding::same(14.0))
}

fn flat_button(ui: &mut egui::Ui, text: &str) -> egui::Response {
    ui.add(flat_button_widget(text))
}

fn flat_button_sized(ui: &mut egui::Ui, text: &str, size: egui::Vec2) -> egui::Response {
    ui.add_sized(size, flat_button_widget(text))
}

fn danger_button(ui: &mut egui::Ui, text: &str) -> egui::Response {
    ui.add(
        egui::Button::new(
            egui::RichText::new(text)
                .strong()
                .size(17.0)
                .color(egui::Color32::WHITE),
        )
        .fill(egui::Color32::from_rgb(198, 76, 76))
        .rounding(egui::Rounding::same(14.0)),
    )
}

fn resolve_tharness_root() -> PathBuf {
    if let Ok(exe) = env::current_exe() {
        if let Some(root) = root_from_exe(&exe) {
            return root;
        }
    }

    env::current_dir().unwrap_or_else(|_| PathBuf::from("."))
}

fn root_from_exe(exe: &Path) -> Option<PathBuf> {
    let parent = exe.parent()?;
    if parent.file_name().is_some_and(|name| name == "bin") {
        return parent.parent().map(Path::to_path_buf);
    }

    for ancestor in exe.ancestors() {
        if ancestor.join("AIGC").join("INDEX.md").exists()
            && ancestor.join("tools").join("tharness.py").exists()
        {
            return Some(ancestor.to_path_buf());
        }
    }

    None
}

fn validate_tharness_root(root: &Path) -> bool {
    root.join("AIGC").join("INDEX.md").exists() && root.join("tools").join("tharness.py").exists()
}

fn anchor_dir(project_root: &Path) -> PathBuf {
    project_root.join(ANCHOR_DIR)
}

enum BindOutcome {
    Written,
    Unchanged,
}

enum BindError {
    WouldOverwrite(PathBuf),
    Io(io::Error),
}

impl From<io::Error> for BindError {
    fn from(value: io::Error) -> Self {
        Self::Io(value)
    }
}

fn bind_project(
    tharness_root: &Path,
    project_root: &Path,
    force: bool,
) -> Result<BindOutcome, BindError> {
    let anchor = anchor_dir(project_root);
    fs::create_dir_all(&anchor)?;

    let files = [
        (
            anchor.join(MANIFEST_NAME),
            manifest_content(tharness_root, project_root),
        ),
        (
            anchor.join("start.ps1"),
            powershell_launcher_content(tharness_root),
        ),
        (
            anchor.join("start.cmd"),
            cmd_launcher_content(tharness_root),
        ),
        (anchor.join("README.md"), readme_content(tharness_root)),
    ];

    let mut changed = false;
    for (path, content) in files {
        changed |= write_generated_file(&path, &content, force)?;
    }
    changed |= write_agents_bridge(project_root, tharness_root)?;

    Ok(if changed {
        BindOutcome::Written
    } else {
        BindOutcome::Unchanged
    })
}

fn write_generated_file(path: &Path, content: &str, force: bool) -> Result<bool, BindError> {
    if path.exists() {
        let existing = fs::read_to_string(path)?;
        if existing == content {
            return Ok(false);
        }
        if !force {
            return Err(BindError::WouldOverwrite(path.to_path_buf()));
        }
    }

    fs::write(path, content)?;
    Ok(true)
}

fn write_agents_bridge(project_root: &Path, tharness_root: &Path) -> Result<bool, BindError> {
    let path = project_root.join(AGENTS_NAME);
    let existing = if path.exists() {
        fs::read_to_string(&path)?
    } else {
        String::new()
    };
    let content = merge_agents_content(&existing, &agents_bridge_content(tharness_root));
    if existing == content {
        return Ok(false);
    }
    fs::write(path, content)?;
    Ok(true)
}

fn merge_agents_content(existing: &str, block: &str) -> String {
    if let (Some(start), Some(end)) = (
        existing.find(AGENTS_BLOCK_START),
        existing.find(AGENTS_BLOCK_END),
    ) {
        if end >= start {
            let end = end + AGENTS_BLOCK_END.len();
            let mut merged = String::new();
            merged.push_str(existing[..start].trim_end());
            if !merged.is_empty() {
                merged.push_str("\n\n");
            }
            merged.push_str(block.trim_end());
            let tail = existing[end..].trim_start();
            if !tail.is_empty() {
                merged.push('\n');
                merged.push_str(tail);
            }
            if !merged.ends_with('\n') {
                merged.push('\n');
            }
            return merged;
        }
    }

    if existing.trim().is_empty() {
        return block.to_owned();
    }

    format!("{}\n\n{}", existing.trim_end(), block)
}

fn agents_bridge_content(tharness_root: &Path) -> String {
    format!(
        concat!(
            "{}\n",
            "# THarness 绑定入口\n",
            "\n",
            "本项目已绑定到 THarness 主工程。AI 在本项目启动后，必须先读取并遵守以下入口：\n",
            "\n",
            "1. `{}`\n",
            "2. `{}`\n",
            "\n",
            "启动边界：\n",
            "\n",
            "- 通用框架、角色、规则、wiki、capabilities 和工具改动写回 THarness 主工程。\n",
            "- 项目事实、项目代码、项目资源和项目专属决策只写入当前目标项目。\n",
            "- 如果当前 AI 环境无法读取 THarness 主工程路径，应先向用户请求把 THarness 主工程加入可读工作区或提供入口内容。\n",
            "\n",
            "{}\n"
        ),
        AGENTS_BLOCK_START,
        tharness_root.join("AGENTS.md").display(),
        tharness_root.join("AIGC").join("INDEX.md").display(),
        AGENTS_BLOCK_END
    )
}

fn manifest_content(tharness_root: &Path, project_root: &Path) -> String {
    format!(
        concat!(
            "# Generated by THarness. This file points this project to the main framework.\n",
            "tharness_root: {}\n",
            "project_root: {}\n",
            "framework_entry: AIGC/INDEX.md\n",
            "role_entry: AIGC/roles/INDEX.md\n",
            "wiki_entry: AIGC/wiki/INDEX.md\n",
            "write_policy: framework_changes_go_to_tharness_root_project_facts_stay_in_project\n",
            "\n"
        ),
        tharness_root.display(),
        project_root.display()
    )
}

fn powershell_launcher_content(tharness_root: &Path) -> String {
    let tool = tharness_root.join("tools").join("tharness.py");
    format!(
        concat!(
            "$ErrorActionPreference = \"Stop\"\n",
            "$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path\n",
            "$ProjectRoot = Split-Path -Parent $ScriptDir\n",
            "$TharnessTool = '{}'\n",
            "$Python = (Get-Command python -ErrorAction SilentlyContinue).Source\n",
            "if (-not $Python) {{ Write-Error \"Python was not found in PATH.\" }}\n",
            "& $Python $TharnessTool project start --root $ProjectRoot\n"
        ),
        ps_single_quote(&tool.display().to_string())
    )
}

fn cmd_launcher_content(tharness_root: &Path) -> String {
    let tool = tharness_root.join("tools").join("tharness.py");
    format!(
        concat!(
            "@echo off\n",
            "set \"PROJECT_ROOT=%~dp0..\"\n",
            "where python >nul 2>nul\n",
            "if %ERRORLEVEL%==0 (\n",
            "  python \"{}\" project start --root \"%PROJECT_ROOT%\"\n",
            ") else (\n",
            "  echo Python was not found in PATH.\n",
            "  exit /b 1\n",
            ")\n",
            "exit /b %ERRORLEVEL%\n"
        ),
        tool.display()
    )
}

fn readme_content(tharness_root: &Path) -> String {
    format!(
        concat!(
            "# THarness Project Anchor\n",
            "\n",
            "This directory is a lightweight launcher for the shared THarness framework.\n",
            "It does not copy `AIGC/`; it only points this project to the main framework root.\n",
            "\n",
            "## Start\n",
            "\n",
            "```powershell\n",
            ".\\.tharness\\start.ps1\n",
            "```\n",
            "\n",
            "## Main Framework\n",
            "\n",
            "`{}`\n",
            "\n",
            "Framework, role, wiki, capability, and tool improvements should be made in the main framework root.\n",
            "Project facts and project-specific code should stay in the current project.\n"
        ),
        tharness_root.display()
    )
}

fn ps_single_quote(value: &str) -> String {
    value.replace('\'', "''")
}
