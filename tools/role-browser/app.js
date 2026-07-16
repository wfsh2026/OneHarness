const state = {
  data: null,
  selected: null,
  currentDocument: null,
  csrfToken: null,
  dirty: false,
  saving: false,
  preview: null,
  documentCache: new Map(),
};
const $ = (id) => document.getElementById(id);

function setText(id, value) { $(id).textContent = value ?? "—"; }

function roleSearchText(role) {
  return [role.displayName, role.slug, role.typeLabel, role.capabilityName, role.capabilityDescription, role.scenario]
    .join(" ").toLocaleLowerCase("zh-CN");
}

function maturityClass(maturity) {
  if (maturity === "evaluated" || maturity === "tested") return "";
  if (maturity === "contracted") return "medium";
  return "developing";
}

function confirmDiscard() {
  return !state.dirty || window.confirm("角色规则有未保存修改，确定放弃这些修改吗？");
}

function updateSaveButton() {
  const maintenance = $("maintenance-mode").checked;
  $("preview-rule").disabled = state.saving || !state.dirty || !maintenance || state.currentDocument?.kind !== "rule";
  $("save-rule").disabled = state.saving || !state.dirty || !maintenance || !state.preview?.changed || state.currentDocument?.kind !== "rule";
}

function setDirty(dirty) {
  state.dirty = dirty;
  if (!dirty) state.preview = null;
  $("dirty-state").textContent = dirty ? "有未保存修改" : "已保存";
  $("dirty-state").classList.toggle("dirty", dirty);
  updateSaveButton();
}

function editorText(content) {
  return content.replace(/\r\n?/g, "\n");
}

function filteredRoles() {
  const query = $("search").value.trim().toLocaleLowerCase("zh-CN");
  const type = $("type-filter").value;
  const capability = $("capability-filter").value;
  return state.data.roles.filter((role) =>
    (!query || roleSearchText(role).includes(query)) &&
    (!type || role.type === type) &&
    (!capability || role.capabilityId === capability)
  );
}

function renderRoles() {
  const roles = filteredRoles();
  const list = $("role-list");
  list.replaceChildren();
  setText("result-count", `${roles.length} 项`);
  $("empty-state").classList.toggle("hidden", roles.length !== 0);
  roles.forEach((role) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = `role-card${state.selected?.slug === role.slug ? " active" : ""}`;
    button.setAttribute("aria-pressed", state.selected?.slug === role.slug ? "true" : "false");
    const name = document.createElement("strong");
    name.textContent = role.displayName;
    const slug = document.createElement("code");
    slug.textContent = role.slug;
    const meta = document.createElement("div");
    const type = document.createElement("span");
    type.textContent = role.typeLabel;
    const maturity = document.createElement("span");
    maturity.className = `confidence-badge ${maturityClass(role.maturity)}`.trim();
    maturity.textContent = `成熟度 ${role.maturityLabel}`;
    meta.append(type, maturity);
    button.append(name, slug, meta);
    button.addEventListener("click", () => selectRole(role));
    list.append(button);
  });
}

function selectRole(role) {
  if (state.selected?.slug === role.slug) return;
  if (!confirmDiscard()) return;
  state.selected = role;
  state.currentDocument = null;
  setDirty(false);
  renderRoles();
  $("detail-empty").classList.add("hidden");
  $("detail-content").classList.remove("hidden");
  setText("detail-type", role.typeLabel);
  setText("detail-confidence", `成熟度 ${role.maturityLabel}`);
  $("detail-confidence").className = `confidence-badge ${maturityClass(role.maturity)}`.trim();
  setText("detail-name", role.displayName);
  setText("detail-slug", role.slug);
  setText("detail-capability", role.capabilityName);
  setText("detail-capability-description", role.capabilityDescription);
  setText("detail-scenario", role.scenario);
  setText("detail-rule", role.ruleEntry);
  setText("detail-route", role.routeEntry || "无独立路由入口");
  $("document-view").classList.add("hidden");
  $("document-state").className = "document-state";
  setText("document-state", "请选择要查看的文档。");
  renderDocumentTabs(role);
}

function renderDocumentTabs(role) {
  const tabs = $("document-tabs");
  tabs.replaceChildren();
  role.documents.forEach((docInfo) => {
    const button = document.createElement("button");
    button.type = "button";
    button.role = "tab";
    button.textContent = docInfo.label;
    button.setAttribute("aria-selected", "false");
    button.addEventListener("click", () => loadDocument(role, docInfo, button));
    tabs.append(button);
  });
}

async function loadDocument(role, docInfo, button) {
  const cacheKey = `${role.slug}/${docInfo.kind}`;
  if (state.currentDocument?.cacheKey !== cacheKey && !confirmDiscard()) return;
  $("document-tabs").querySelectorAll("button").forEach((item) => item.setAttribute("aria-selected", String(item === button)));
  $("document-view").classList.add("hidden");
  $("document-state").className = "document-state";
  setText("document-state", "正在从本地读取…");
  try {
    let payload = state.documentCache.get(cacheKey);
    if (!payload) {
      const response = await fetch(`/api/roles/${encodeURIComponent(role.slug)}/documents/${docInfo.kind}`);
      payload = await response.json();
      if (!response.ok) throw new Error(payload.error || "文档读取失败");
      state.documentCache.set(cacheKey, payload);
    }
    if (state.selected?.slug !== role.slug) return;
    state.currentDocument = { ...payload, cacheKey, editorContent: editorText(payload.content) };
    setDirty(false);
    $("document-state").classList.add("hidden");
    $("document-view").classList.remove("hidden");
    setText("document-title", payload.label);
    setText("document-path", payload.path);
    const editingRule = payload.kind === "rule";
    $("document-content").classList.toggle("hidden", editingRule);
    $("rule-editor").classList.toggle("hidden", !editingRule);
    if (editingRule) {
      $("rule-content").value = state.currentDocument.editorContent;
      setText("save-status", "可编辑；保存时会检查文件版本冲突。");
      $("save-status").className = "";
    } else {
      setText("document-content", payload.content);
    }
  } catch (error) {
    $("document-state").className = "document-state error";
    setText("document-state", `读取失败：${error.message}`);
  }
}

async function previewRule() {
  if (!state.currentDocument || !state.dirty || state.saving || !$("maintenance-mode").checked) return;
  state.saving = true;
  updateSaveButton();
  setText("save-status", "正在生成差异与影响计划…");
  try {
    const response = await fetch(`/api/roles/${encodeURIComponent(state.selected.slug)}/documents/rule`, {
      method: "PUT",
      headers: {"Content-Type": "application/json", "X-Tharness-CSRF": state.csrfToken},
      body: JSON.stringify({content: $("rule-content").value, baseHash: state.currentDocument.hash, previewOnly: true}),
    });
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || "预览失败");
    state.preview = payload;
    $("maintenance-impact").textContent = [payload.diff, "", "受影响入口:", ...payload.affectedEntries, "", "版本:", payload.versionPolicy, "", "自检:", ...payload.selfCheckPlan].join("\n");
    $("maintenance-impact").classList.remove("hidden");
    setText("save-status", "差异已预览；确认后可保存。保存不会自动更新其他入口。 ");
  } catch (error) {
    state.preview = null;
    setText("save-status", error.message);
    $("save-status").className = "error";
  } finally {
    state.saving = false;
    updateSaveButton();
  }
}

async function saveRule() {
  if (!state.currentDocument || state.currentDocument.kind !== "rule" || !state.dirty || state.saving) return;
  state.saving = true;
  updateSaveButton();
  setText("save-status", "正在保存…");
  $("save-status").className = "";
  try {
    const response = await fetch(
      `/api/roles/${encodeURIComponent(state.selected.slug)}/documents/rule`,
      {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "X-Tharness-CSRF": state.csrfToken,
        },
        body: JSON.stringify({
          content: $("rule-content").value,
          baseHash: state.currentDocument.hash,
          maintenanceMode: $("maintenance-mode").checked,
          acknowledgeImpact: Boolean(state.preview?.changed),
        }),
      },
    );
    const payload = await response.json();
    if (!response.ok) throw new Error(response.status === 409 ? `保存冲突：${payload.error}` : payload.error || "保存失败");
    const cacheKey = state.currentDocument.cacheKey;
    state.currentDocument = { ...payload, cacheKey, editorContent: editorText(payload.content) };
    state.documentCache.set(cacheKey, payload);
    $("rule-content").value = state.currentDocument.editorContent;
    setDirty(false);
    setText("save-status", "保存成功，文件版本已更新。");
    $("maintenance-impact").classList.add("hidden");
  } catch (error) {
    $("save-status").className = "error";
    setText("save-status", error.message);
  } finally {
    state.saving = false;
    updateSaveButton();
  }
}

function populateFilters(data) {
  data.roleTypes.forEach((type) => $("type-filter").add(new Option(type.label, type.id)));
  data.capabilities
    .filter((capability) => data.roles.some((role) => role.capabilityId === capability.id))
    .forEach((capability) => $("capability-filter").add(new Option(capability.name, capability.id)));
}

async function init() {
  try {
    const response = await fetch("/api/summary");
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "角色数据加载失败");
    state.data = data;
    state.csrfToken = data.csrfToken;
    setText("role-count", data.counts.roles);
    setText("system-version", data.systemVersion);
    setText("dispatchable-count", data.counts.dispatchable);
    setText("capability-count", data.counts.capabilities);
    populateFilters(data);
    renderRoles();
  } catch (error) {
    $("role-list").innerHTML = "";
    $("empty-state").className = "state-card";
    setText("empty-state", `加载失败：${error.message}。请停止工具并运行 Tharness 自检。`);
  }
}

["search", "type-filter", "capability-filter"].forEach((id) => $(id).addEventListener("input", renderRoles));
$("rule-content").addEventListener("input", () => {
  if (state.currentDocument?.kind === "rule") {
    state.preview = null;
    $("maintenance-impact").classList.add("hidden");
    setDirty($("rule-content").value !== state.currentDocument.editorContent);
  }
});
$("save-rule").addEventListener("click", saveRule);
$("preview-rule").addEventListener("click", previewRule);
$("maintenance-mode").addEventListener("change", () => {
  state.preview = null;
  $("maintenance-impact").classList.add("hidden");
  updateSaveButton();
});
document.addEventListener("keydown", (event) => {
  if ((event.ctrlKey || event.metaKey) && event.key.toLocaleLowerCase() === "s" && state.currentDocument?.kind === "rule") {
    event.preventDefault();
    saveRule();
  }
});
window.addEventListener("beforeunload", (event) => {
  if (!state.dirty) return;
  event.preventDefault();
  event.returnValue = "";
});
init();
