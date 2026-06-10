const API = {
  TOKEN_KEY: "biocraft_access_token",

  getToken() {
    return localStorage.getItem(this.TOKEN_KEY);
  },

  setToken(token) {
    localStorage.setItem(this.TOKEN_KEY, token);
  },

  clearToken() {
    localStorage.removeItem(this.TOKEN_KEY);
  },

  isLoggedIn() {
    return !!this.getToken();
  },

  async request(method, path, body) {
    const headers = { "Content-Type": "application/json" };
    const token = this.getToken();
    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }

    const res = await fetch(path, {
      method,
      headers,
      body: body ? JSON.stringify(body) : undefined,
    });

    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.detail || "Request failed");
    }
    return data;
  },

  async login(username, password) {
    const formData = new URLSearchParams();
    formData.append("username", username);
    formData.append("password", password);

    const res = await fetch("/auth/token", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: formData,
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Login failed");
    this.setToken(data.access_token);
    return data;
  },

  async register(username, email, password) {
    return this.request("POST", "/auth/register", {
      username,
      email,
      password,
    });
  },

  async getMe() {
    return this.request("GET", "/users/me");
  },

  logout() {
    this.clearToken();
    window.location.href = "/";
  },
};
