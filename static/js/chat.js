const CHAT_HTML = `
<div id="chat-widget" class="fixed bottom-6 right-6 z-50" style="display:none">
  <button id="chat-toggle"
    class="w-14 h-14 bg-[#00dce5] text-[#002021] rounded-2xl flex items-center justify-center shadow-[0_0_25px_rgba(0,220,229,0.3)] hover:shadow-[0_0_35px_rgba(0,220,229,0.5)] hover:scale-105 transition-all active:scale-95">
    <span class="material-symbols-outlined text-2xl" id="chat-icon">smart_toy</span>
  </button>

  <div id="chat-panel" class="hidden fixed bottom-24 right-6 w-[380px] max-w-[calc(100vw-48px)] h-[520px] max-h-[calc(100vh-160px)] rounded-2xl flex flex-col overflow-hidden shadow-[0_0_40px_rgba(0,0,0,0.5)]"
    style="background:rgba(16,20,21,0.96);backdrop-filter:blur(20px);border:1px solid rgba(255,255,255,0.08)">
    <div class="p-4 border-b border-white/10 flex items-center gap-3">
      <div class="w-8 h-8 rounded-full bg-[#00dce5]/20 flex items-center justify-center">
        <span class="material-symbols-outlined text-[#00dce5] text-lg">smart_toy</span>
      </div>
      <div class="flex-1">
        <div style="font-family:'JetBrains Mono',monospace;font-size:14px;color:#e0e3e5">BIOCRAFT Assistant</div>
        <div class="flex items-center gap-1" style="font-family:'JetBrains Mono',monospace;font-size:12px;color:#2ae500">
          <span class="w-1.5 h-1.5 rounded-full bg-[#2ae500]"></span> Online
        </div>
      </div>
      <button onclick="chat.hide()" class="text-[#c7c6cd] hover:text-white">
        <span class="material-symbols-outlined">close</span>
      </button>
    </div>
    <div id="chat-messages" class="flex-1 overflow-y-auto p-4 space-y-4"></div>
    <div class="p-4 border-t border-white/10">
      <div class="flex gap-2">
        <input id="chat-input"
          class="flex-1 bg-[#0b0f10] border border-white/10 rounded-xl px-4 py-3 text-sm text-[#e0e3e5] outline-none focus:border-[#00dce5]/50 focus:ring-1 focus:ring-[#00dce5]/30"
          placeholder="Type a message..." style="font-family:'Hanken Grotesk',sans-serif">
        <button id="chat-send"
          class="px-4 py-3 bg-[#00dce5] text-[#002021] rounded-xl font-bold text-sm hover:shadow-[0_0_20px_rgba(0,220,229,0.4)] transition-all">
          <span class="material-symbols-outlined text-xl">send</span>
        </button>
      </div>
    </div>
  </div>
</div>`;

const chat = {
  messages: [],
  loading: false,

  init() {
    document.body.insertAdjacentHTML("beforeend", CHAT_HTML);
    document.getElementById("chat-widget").style.display = "block";

    document.getElementById("chat-toggle").onclick = () => this.toggle();
    document.getElementById("chat-send").onclick = () => this.sendMessage();
    document.getElementById("chat-input").onkeydown = (e) => {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        this.sendMessage();
      }
    };

    this.addMessage("bot", "Welcome to Biocraft Digital. How may I assist you today?");
  },

  toggle() {
    const panel = document.getElementById("chat-panel");
    const icon = document.getElementById("chat-icon");
    const isOpen = !panel.classList.contains("hidden");
    panel.classList.toggle("hidden");
    icon.textContent = isOpen ? "smart_toy" : "close";
    if (!isOpen) {
      setTimeout(() => this.scrollToBottom(), 50);
      document.getElementById("chat-input").focus();
    }
  },

  hide() {
    document.getElementById("chat-panel").classList.add("hidden");
    document.getElementById("chat-icon").textContent = "smart_toy";
  },

  scrollToBottom() {
    const el = document.getElementById("chat-messages");
    el.scrollTop = el.scrollHeight;
  },

  addMessage(role, text) {
    const container = document.getElementById("chat-messages");
    const isUser = role === "user";
    const bubble = document.createElement("div");
    bubble.className = `flex ${isUser ? "justify-end" : "justify-start"} mb-3`;
    bubble.innerHTML = `
      <div class="max-w-[80%] rounded-2xl ${
        isUser
          ? "rounded-tr-sm bg-[#00dce5] text-[#002021]"
          : "rounded-tl-sm"
      } px-4 py-3 text-sm leading-relaxed`
      + ` style="${isUser ? "" : "background:rgba(255,255,255,0.06);color:#e0e3e5"}"`
      + `>${text.replace(/\n/g, "<br>")}</div>`;
    container.appendChild(bubble);
    this.scrollToBottom();
  },

  showLoading() {
    this.loading = true;
    const container = document.getElementById("chat-messages");
    const div = document.createElement("div");
    div.id = "chat-loading";
    div.className = "flex justify-start mb-3";
    div.innerHTML =
      '<div class="bg-[rgba(255,255,255,0.06)] rounded-2xl rounded-tl-sm px-4 py-3 flex gap-1">'
      + '<span class="w-2 h-2 bg-[#c7c6cd]/40 rounded-full animate-bounce"></span>'
      + '<span class="w-2 h-2 bg-[#c7c6cd]/40 rounded-full animate-bounce" style="animation-delay:0.1s"></span>'
      + '<span class="w-2 h-2 bg-[#c7c6cd]/40 rounded-full animate-bounce" style="animation-delay:0.2s"></span>'
      + "</div>";
    container.appendChild(div);
    this.scrollToBottom();
  },

  hideLoading() {
    this.loading = false;
    const el = document.getElementById("chat-loading");
    if (el) el.remove();
  },

  async sendMessage() {
    if (this.loading) return;
    const input = document.getElementById("chat-input");
    const text = input.value.trim();
    if (!text) return;

    input.value = "";
    this.addMessage("user", text);
    this.showLoading();

    try {
      const res = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text }),
      });
      const data = await res.json();
      this.hideLoading();
      this.addMessage("bot", data.reply);
    } catch {
      this.hideLoading();
      this.addMessage("bot", "Connection error. Please try again.");
    }
  },
};

document.addEventListener("DOMContentLoaded", () => chat.init());
