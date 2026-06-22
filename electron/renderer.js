const apiBase = "http://127.0.0.1:8000/api";

const authSection = document.getElementById("auth-section");
const vaultSection = document.getElementById("vault-section");
const loginTab = document.getElementById("login-tab");
const registerTab = document.getElementById("register-tab");
const authForm = document.getElementById("auth-form");
const authSubmit = document.getElementById("auth-submit");
const authHint = document.getElementById("auth-hint");
const registerExtra = document.getElementById("register-extra");
const authEmail = document.getElementById("auth-email");
const authPassword = document.getElementById("auth-password");
const authConfirmPassword = document.getElementById("auth-confirm-password");
const vaultList = document.getElementById("vault-list");
const vaultName = document.getElementById("vault-name");
const entryList = document.getElementById("entry-list");
const modal = document.getElementById("modal");
const modalBody = document.getElementById("modal-body");
const closeModal = document.getElementById("close-modal");
const refreshVaultsButton = document.getElementById("refresh-vaults");
const newVaultButton = document.getElementById("new-vault-button");
const addEntryButton = document.getElementById("add-entry-button");
const entriesCard = document.getElementById("entries-card");

let authMode = "login";
let accessToken = null;
let selectedVault = null;

loginTab.addEventListener("click", () => setAuthMode("login"));
registerTab.addEventListener("click", () => setAuthMode("register"));
authForm.addEventListener("submit", handleAuthSubmit);
refreshVaultsButton.addEventListener("click", loadVaults);
newVaultButton.addEventListener("click", openCreateVaultModal);
addEntryButton.addEventListener("click", openAddEntryModal);
closeModal.addEventListener("click", closeDialog);

function setAuthMode(mode) {
  authMode = mode;
  loginTab.classList.toggle("active", mode === "login");
  registerTab.classList.toggle("active", mode === "register");
  registerExtra.classList.toggle("hidden", mode !== "register");
  authSubmit.textContent = mode === "login" ? "Login" : "Register";
  authHint.textContent = mode === "login"
    ? "Enter your account credentials to sign in."
    : "Create a new account with a strong master password.";
}

function showDialog(content) {
  modalBody.innerHTML = "";
  modalBody.appendChild(content);
  modal.classList.remove("hidden");
}

function closeDialog() {
  modal.classList.add("hidden");
}

function getAuthHeaders() {
  return {
    Authorization: `Bearer ${accessToken}`,
    "Content-Type": "application/json",
  };
}

async function handleAuthSubmit(event) {
  event.preventDefault();

  const email = authEmail.value.trim();
  const password = authPassword.value.trim();

  if (!email || !password) return;
  if (authMode === "register") {
    const confirm = authConfirmPassword.value.trim();
    if (password !== confirm) {
      return alert("Passwords do not match.");
    }
  }

  const route = authMode === "login" ? "/auth/login" : "/auth/register";
  const response = await fetch(`${apiBase}${route}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      email,
      master_password: password,
    }),
  });

  if (!response.ok) {
    const body = await response.json();
    return alert(body.detail || "Authentication failed.");
  }

  const data = await response.json();
  accessToken = data.access_token;
  authSection.classList.add("hidden");
  vaultSection.classList.remove("hidden");
  await loadVaults();
}

async function loadVaults() {
  if (!accessToken) return;

  const response = await fetch(`${apiBase}/vault/`, {
    headers: getAuthHeaders(),
  });

  if (!response.ok) {
    return alert("Unable to load vaults.");
  }

  const vaults = await response.json();
  vaultList.innerHTML = "";
  selectedVault = null;
  entryList.innerHTML = "";
  vaultName.textContent = "";

  for (const vault of vaults) {
    const card = document.createElement("div");
    card.className = "vault-card";
    card.innerHTML = `
      <h3>${vault.name}</h3>
      <p>${vault.description || "No description"}</p>
      <small>${new Date(vault.created_at).toLocaleString()}</small>
    `;
    card.addEventListener("click", () => selectVault(vault));
    vaultList.appendChild(card);
  }
}

async function selectVault(vault) {
  selectedVault = vault;
  vaultName.textContent = `Vault: ${vault.name}`;
  entriesCard.classList.remove("hidden");
  await loadEntries(vault.id);
}

async function loadEntries(vaultId) {
  if (!accessToken || !vaultId) return;

  const response = await fetch(`${apiBase}/vault/${vaultId}/entries`, {
    headers: getAuthHeaders(),
  });

  if (!response.ok) {
    return alert("Unable to load vault entries.");
  }

  const entries = await response.json();
  entryList.innerHTML = "";

  for (const entry of entries) {
    const card = document.createElement("div");
    card.className = "entry-card";
    card.innerHTML = `
      <h3>${entry.title}</h3>
      <p>${entry.username || "No username"}</p>
      <p>${entry.url || "No URL"}</p>
      <p>Score: ${entry.strength_score}</p>
      <p>Status: ${entry.breach_status}</p>
      <button class="secondary">Decrypt Password</button>
    `;

    card.querySelector("button").addEventListener("click", () => openDecryptModal(entry));
    entryList.appendChild(card);
  }
}

function openCreateVaultModal() {
  const form = document.createElement("form");
  form.innerHTML = `
    <h3>Create New Vault</h3>
    <label>Name</label>
    <input id="new-vault-name" required />
    <label>Description</label>
    <textarea id="new-vault-description"></textarea>
    <button type="submit">Create Vault</button>
  `;

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const name = form.querySelector("#new-vault-name").value.trim();
    const description = form.querySelector("#new-vault-description").value.trim();

    const response = await fetch(`${apiBase}/vault/`, {
      method: "POST",
      headers: getAuthHeaders(),
      body: JSON.stringify({ name, description }),
    });

    if (!response.ok) {
      const body = await response.json();
      return alert(body.detail || "Unable to create vault.");
    }

    closeDialog();
    await loadVaults();
  });

  showDialog(form);
}

function openAddEntryModal() {
  if (!selectedVault) return alert("Select a vault first.");

  const form = document.createElement("form");
  form.innerHTML = `
    <h3>Add Entry to ${selectedVault.name}</h3>
    <label>Title</label>
    <input id="entry-title" required />
    <label>Username</label>
    <input id="entry-username" />
    <label>URL</label>
    <input id="entry-url" />
    <label>Password</label>
    <input id="entry-password" required minlength="8" />
    <label>Notes</label>
    <textarea id="entry-notes"></textarea>
    <label>Master Password</label>
    <input id="entry-master-password" type="password" required minlength="12" />
    <button type="submit">Create Entry</button>
  `;

  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const title = form.querySelector("#entry-title").value.trim();
    const username = form.querySelector("#entry-username").value.trim();
    const url = form.querySelector("#entry-url").value.trim();
    const password = form.querySelector("#entry-password").value.trim();
    const notes = form.querySelector("#entry-notes").value.trim();
    const masterPassword = form.querySelector("#entry-master-password").value.trim();

    const response = await fetch(`${apiBase}/vault/entry`, {
      method: "POST",
      headers: getAuthHeaders(),
      body: JSON.stringify({
        title,
        username,
        url,
        password,
        notes,
        master_password: masterPassword,
        vault_id: selectedVault.id,
      }),
    });

    if (!response.ok) {
      const body = await response.json();
      return alert(body.detail || "Unable to create entry.");
    }

    closeDialog();
    await loadEntries(selectedVault.id);
  });

  showDialog(form);
}

function openDecryptModal(entry) {
  const form = document.createElement("form");
  form.innerHTML = `
    <h3>Decrypt Entry</h3>
    <p>${entry.title}</p>
    <label>Master Password</label>
    <input id="decrypt-master-password" type="password" required minlength="12" />
    <button type="submit">Decrypt</button>
  `;

  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const masterPassword = form.querySelector("#decrypt-master-password").value.trim();
    const response = await fetch(`${apiBase}/vault/entry/decrypt`, {
      method: "POST",
      headers: getAuthHeaders(),
      body: JSON.stringify({
        entry_id: entry.id,
        vault_id: selectedVault.id,
        master_password: masterPassword,
      }),
    });

    if (!response.ok) {
      const body = await response.json();
      return alert(body.detail || "Unable to decrypt entry.");
    }

    const data = await response.json();
    const result = document.createElement("div");
    result.innerHTML = `<p><strong>Password:</strong> ${data.password}</p>`;
    modalBody.innerHTML = "";
    modalBody.appendChild(result);
  });

  showDialog(form);
}

setAuthMode("login");
