### 0.4.0: 2025-07-17

* Add image generation detection and skip functionality
* Add `disable_for_image_generation` valve (enabled by default)
* Implement official Open WebUI image generation request detection
* Fix time context injection interfering with image generation prompts
* Support ComfyUI workflow detection
* Improve image generation quality by preventing prompt contamination

### 0.3.0: 2025-07-16

* Fix possible regression when sending an image

### 0.2.0: 2025-07-16

- Fix TypeError when handling multimodal content (list vs string)
- Add proper type checking for message content
- Add multimodal content support (text + images)
- Enhance error handling for various input types

### 0.1.0: 2025-07-16

- Initial release of Time Awareness Filter
- Add automatic time context injection into user messages
- Add timezone awareness with user-specific configuration
- Add user valve configuration for personalization
- Add system valve configuration for default settings
- Add BeautifulSoup XML parsing for context management
- Privacy-focused local processing (no external API calls)
