## 🕙 Open WebUI Memory function

### An [Open WebUI](https://github.com/open-webui/open-webui) filter that automatically adds time context to user messages, enabling AI assistants to be aware of the current time and date in conversations.

![Open WebUI](https://img.shields.io/badge/Open%20WebUI-222222?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyBmaWxsPSIjZmZmZmZmIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGhlaWdodD0iMWVtIiBzdHlsZT0iZmxleDpub25lO2xpbmUtaGVpZ2h0OjEiIHZpZXdCb3g9IjAgMCAyNCAyNCIgd2lkdGg9IjFlbSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cGF0aCBjbGlwLXJ1bGU9ImV2ZW5vZGQiIGQ9Ik0xNy42OTcgMTJjMCA0Ljk3LTMuOTYyIDktOC44NDkgOUMzLjk2MiAyMSAwIDE2Ljk3IDAgMTJzMy45NjItOSA4Ljg0OC05YzQuODg3IDAgOC44NDkgNC4wMyA4Ljg0OSA5em0tMy42MzYgMGMwIDIuOTI4LTIuMzM0IDUuMzAxLTUuMjEzIDUuMzAxLTIuODc4IDAtNS4yMTItMi4zNzMtNS4yMTItNS4zMDFTNS45NyA2LjY5OSA4Ljg0OCA2LjY5OWMyLjg4IDAgNS4yMTMgMi4zNzMgNS4yMTMgNS4zMDF6Ij48L3BhdGg+PHBhdGggZD0iTTI0IDNoLTMuMzk0djE4SDI0VjN6Ij48L3BhdGg+PC9zdmc+Cg==)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Version](https://img.shields.io/badge/version-0.3.0-blue?style=for-the-badge)

## ✨ Features

- **Automatic time injection**: Seamlessly adds current time context to user messages
- **Timezone awareness**: Supports user-specific and system timezone configuration
- **Multimodal support**: Handles text and image content properly
- **User customization**: Configurable through user valves
- **Privacy-focused**: No external API calls, all processing happens locally

## 🧠 How it works

The filter automatically injects time context into user messages, allowing AI assistants to:
- Understand when messages are sent
- Provide time-relevant responses
- Format dates and times appropriately
- Consider context like "today", "yesterday", "this week", etc.

## 📦 Installation

1. Add `time-awareness.py` to your Open WebUI Functions
2. Ensure dependencies are installed:
   ```bash
   pip install beautifulsoup4 lxml
   ```

## ⚙️ Configuration

### System Valves
- **Timezone**: Default system timezone (e.g., "UTC", "Europe/Helsinki")
- **Priority**: Filter execution priority (default: -10)

### User Valves
- **Timezone**: Personal timezone override
- **Enabled**: Toggle to enable/disable the filter per user

## 🔧 Dependencies

- `beautifulsoup4` - For parsing HTML/XML content
- `lxml` - XML parser for BeautifulSoup (install with `pip install lxml`)

## 📝 Example

When a user sends: "What's the weather like today?"

The filter automatically adds time context:
```xml
<details type="filters_context">
<summary>Filters context</summary>
<context id="time_awareness">
<time timezone="Europe/Helsinki" format="%a %d %b %Y, %H:%M:%S">
<!-- System timezone -->Mon 16 Jul 2025, 20:15:30
</time>
</context>
</details>
```

## 🐛 Troubleshooting

### Common Issues

1. **BeautifulSoup XML parser error**: Install lxml with `pip install lxml`
2. **Timezone not recognized**: Check timezone is in `zoneinfo.available_timezones()`
3. **Multimodal content error**: Update to latest version with multimodal support

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

Inspired by the need for time-aware AI conversations in Open WebUI.
