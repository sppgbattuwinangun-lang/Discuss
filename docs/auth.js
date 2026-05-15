/* =========================================================
   SPPG Auth — login admin sederhana berbasis SHA-256 hash
   - Password tersimpan terenkripsi di localStorage
   - Default: admin / sppg2026 (bisa diganti di Pengaturan)
   - Session: localStorage / sessionStorage (rememberMe)
   ========================================================= */
(function () {
  'use strict';

  const STORAGE_KEY = 'sppg_admin_credentials';
  const SESSION_KEY = 'sppg_session';
  const DEFAULT_USER = 'admin';
  const DEFAULT_PASS = 'sppg2026';

  async function sha256(str) {
    const buf = new TextEncoder().encode(str);
    const hash = await crypto.subtle.digest('SHA-256', buf);
    return Array.from(new Uint8Array(hash))
      .map(b => b.toString(16).padStart(2, '0'))
      .join('');
  }

  async function ensureCredentials() {
    let raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) {
      const passHash = await sha256(DEFAULT_PASS);
      const cred = { username: DEFAULT_USER, passHash };
      localStorage.setItem(STORAGE_KEY, JSON.stringify(cred));
      return cred;
    }
    try {
      return JSON.parse(raw);
    } catch (e) {
      const passHash = await sha256(DEFAULT_PASS);
      const cred = { username: DEFAULT_USER, passHash };
      localStorage.setItem(STORAGE_KEY, JSON.stringify(cred));
      return cred;
    }
  }

  async function login(username, password, rememberMe) {
    const cred = await ensureCredentials();
    const passHash = await sha256(password);
    if (
      username.trim().toLowerCase() === cred.username.toLowerCase() &&
      passHash === cred.passHash
    ) {
      const session = {
        username: cred.username,
        loginAt: new Date().toISOString(),
        token: await sha256(cred.username + Date.now() + Math.random()),
      };
      const store = rememberMe ? localStorage : sessionStorage;
      store.setItem(SESSION_KEY, JSON.stringify(session));
      return { ok: true, session };
    }
    return { ok: false, error: 'Username atau password salah.' };
  }

  function logout() {
    localStorage.removeItem(SESSION_KEY);
    sessionStorage.removeItem(SESSION_KEY);
  }

  function getSession() {
    const raw =
      sessionStorage.getItem(SESSION_KEY) || localStorage.getItem(SESSION_KEY);
    if (!raw) return null;
    try {
      return JSON.parse(raw);
    } catch (e) {
      return null;
    }
  }

  function isAuthenticated() {
    return !!getSession();
  }

  async function changePassword(oldPass, newPass) {
    const cred = await ensureCredentials();
    const oldHash = await sha256(oldPass);
    if (oldHash !== cred.passHash) {
      return { ok: false, error: 'Password lama tidak cocok.' };
    }
    if (!newPass || newPass.length < 6) {
      return { ok: false, error: 'Password baru minimal 6 karakter.' };
    }
    const newHash = await sha256(newPass);
    cred.passHash = newHash;
    localStorage.setItem(STORAGE_KEY, JSON.stringify(cred));
    return { ok: true };
  }

  // Expose
  window.SPPGAuth = {
    login,
    logout,
    getSession,
    isAuthenticated,
    changePassword,
    ensureCredentials,
  };
})();
