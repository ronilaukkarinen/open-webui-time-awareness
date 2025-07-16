# Open WebUI Time Awareness Filter

[![Open WebUI](https://img.shields.io/badge/Open%20WebUI-Compatible-blue?style=flat-square&logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTEyIDJDNi40NzcgMiAyIDYuNDc3IDIgMTJTNi40NzcgMjIgMTIgMjIgMjIgMTcuNTIzIDIyIDEyIDIyIDIgMTIgMloiIGZpbGw9IiNmZmYiLz4KPHBhdGggZD0iTTEyIDJDNi40NzcgMiAyIDYuNDc3IDIgMTJTNi40NzcgMjIgMTIgMjIgMjIgMTcuNTIzIDIyIDEyIDIyIDIgMTIgMloiIGZpbGw9IiNmZmYiLz4KPC9zdmc+)](https://github.com/open-webui/open-webui)
[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)](https://www.python.org/)
[![Version](https://img.shields.io/badge/Version-0.2.0-green?style=flat-square)](https://github.com/ronilaukkarinen/open-webui-time-awareness/releases)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

An Open WebUI filter that automatically adds time context to user messages, enabling AI assistants to be aware of the current time and date in conversations.

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