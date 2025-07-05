# 🚁 FPV Caption Creator

Transform your FPV drone flights into engaging social media content with AI-powered caption generation!

## ✨ Features

- **Multi-Platform Support**: Generate captions for Instagram, TikTok, and YouTube Shorts
- **AI-Powered**: Uses Gemini AI via OpenRouter for intelligent caption generation
- **Smart Hashtags**: Automatically generates relevant hashtags for each platform
- **Platform-Specific Optimization**: Tailored content for each social media platform
- **Beautiful UI**: Modern Streamlit interface with custom styling
- **Easy to Use**: Simple input fields for location and flight description

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenRouter API key (for Gemini AI access)

### Installation

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd shorts-caption-creator
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:

   Create a `.env` file in the project root:
   ```bash
   cp env_example.txt .env
   ```

   Edit the `.env` file and add your OpenRouter API key:
   ```
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   ```

4. **Run the application**:
   ```bash
   streamlit run app.py
   ```

5. **Open your browser** and navigate to `http://localhost:8501`

## 🔑 Getting Your OpenRouter API Key

1. Visit [OpenRouter.ai](https://openrouter.ai/)
2. Sign up for an account
3. Navigate to the API Keys section
4. Create a new API key
5. Copy the key and paste it in your `.env` file

## 📱 How to Use

1. **Enter Flight Details**:
   - **Location**: Be specific (e.g., "Malibu Beach, California" instead of just "beach")
   - **Description**: Describe your flight style, maneuvers, lighting, and what makes it special

2. **Select Platforms**:
   - Choose one or more platforms: Instagram, TikTok, or YouTube Shorts
   - Each platform will generate optimized content

3. **Generate Captions**:
   - Click "🚀 Generate Captions"
   - Wait for the AI to create your content
   - Copy and paste the results to your social media posts

## 🎯 Platform-Specific Features

### Instagram
- Engaging visual storytelling
- Emoji integration
- Call-to-action endings
- 150-word limit

### TikTok
- Short and punchy content
- Trending language
- Shareable hooks
- 100-word limit

### YouTube Shorts
- SEO-optimized titles (under 60 characters)
- Descriptive content (under 125 words)
- Keyword integration
- Separate title and description

## 💡 Tips for Better Results

### Location Tips
- Be specific: "Golden Gate Bridge, San Francisco" vs "bridge"
- Include landmarks and unique features
- Mention the type of environment (urban, nature, coastal, etc.)

### Description Tips
- **Flight Style**: "smooth cinematic", "aggressive racing", "freestyle"
- **Lighting**: "golden hour", "blue hour", "overcast", "sunset"
- **Maneuvers**: "power loops", "knife edge", "gap shots", "proximity flying"
- **Emotions**: "heart-pounding", "peaceful", "adrenaline rush"

## 🛠️ Technical Details

### Built With
- **Streamlit**: Web application framework
- **OpenRouter**: API gateway for AI models
- **Gemini Pro**: Google's AI model for text generation
- **Python**: Backend logic and API integration

### Project Structure
```
shorts-caption-creator/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── env_example.txt     # Environment variables template
└── README.md          # This file
```

### API Usage
The application uses OpenRouter's API to access Gemini Pro with the following configuration:
- Model: `google/gemini-pro`
- Max tokens: 300 (captions), 200 (hashtags)
- Temperature: 0.7 (captions), 0.6 (hashtags)

## 🔧 Customization

### Adding New Platforms
To add support for additional platforms:

1. Add a new prompt in the `prompts` dictionary in `generate_caption()`
2. Update the platform selection multiselect widget
3. Add platform-specific parsing logic if needed

### Modifying Prompts
You can customize the AI prompts by editing the `prompts` dictionary in the `FPVCaptionGenerator` class.

### Styling
Custom CSS is included in the `app.py` file. Modify the styles in the `st.markdown()` section to change the appearance.

## 🐛 Troubleshooting

### Common Issues

1. **"OpenRouter API key not found"**:
   - Make sure your `.env` file exists and contains the correct API key
   - Verify the key is valid on OpenRouter.ai

2. **"Error generating caption"**:
   - Check your internet connection
   - Verify your OpenRouter account has sufficient credits
   - Ensure the API key has the correct permissions

3. **Empty or malformed responses**:
   - Try refreshing the page and generating again
   - Check if the input fields contain valid information

### Getting Help

If you encounter issues:
1. Check the error messages in the Streamlit interface
2. Verify your environment variables are set correctly
3. Ensure all dependencies are installed
4. Check the OpenRouter API status

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 🙏 Acknowledgments

- Built for the FPV community
- Powered by Gemini AI
- Made with ❤️ and Streamlit

---

**Happy Flying! 🚁✨**