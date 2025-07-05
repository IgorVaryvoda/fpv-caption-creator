import streamlit as st
import requests
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="FPV Caption Creator",
    page_icon="🚁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #ff6b6b, #4ecdc4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .platform-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 2rem;
        border-radius: 16px;
        margin: 1.5rem 0;
        border: 1px solid #e9ecef;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
    }

    .platform-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
    }

    .hashtag-section {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin-top: 1.5rem;
        border: 1px solid #bae6fd;
        box-shadow: 0 2px 10px rgba(14, 165, 233, 0.1);
    }

    .stButton > button {
        background: linear-gradient(90deg, #ff6b6b, #4ecdc4);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: bold;
        border-radius: 25px;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }

    .platform-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 1rem;
        font-size: 1.2rem;
        font-weight: 600;
        color: #1f2937;
    }

    .caption-box {
        background: #ffffff;
        border: 1px solid #d1d5db;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        line-height: 1.6;
    }

    .hashtag-box {
        background: #fafafa;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        font-family: monospace;
        font-size: 0.9rem;
        color: #1e40af;
    }
</style>
""", unsafe_allow_html=True)

class FPVCaptionGenerator:
    def __init__(self):
        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"

    def generate_caption(self, location, description, platform, model):
        """Generate caption using selected model via OpenRouter"""
        if not self.openrouter_api_key:
            st.error("⚠️ OpenRouter API key not found. Please set OPENROUTER_API_KEY in your environment variables.")
            return None

        # Platform-specific prompts
        prompts = {
            "instagram": f"""
            Create an engaging Instagram caption for an FPV drone video with these details:
            Location: {location}
            Flight description: {description}

            Requirements:
            - Keep it under 150 words
            - Make it exciting and visually descriptive
            - Include relevant emojis
            - Focus on the experience and visuals
            - End with a call to action
            - DO NOT include any hashtags in the caption text

            Format: Just return the caption text, no hashtags, no extra formatting.
            """,

            "tiktok": f"""
            Create a catchy TikTok caption for an FPV drone video with these details:
            Location: {location}
            Flight description: {description}

            Requirements:
            - Keep it short and punchy (under 100 words)
            - Use trending language and emojis
            - Make it shareable and engaging
            - Include a hook at the beginning
            - DO NOT include any hashtags in the caption text

            Format: Just return the caption text, no hashtags, no extra formatting.
            """,

            "youtube_shorts": f"""
            Create both a title and description for a YouTube Shorts FPV drone video:
            Location: {location}
            Flight description: {description}

            Requirements:
            - Title: Under 60 characters, clickable and SEO-friendly
            - Description: Under 125 words, informative but engaging
            - Include relevant keywords for discoverability
            - DO NOT include any hashtags in the title or description

            Format:
            TITLE: [your title here]
            DESCRIPTION: [your description here]
            """
        }

        headers = {
            "Authorization": f"Bearer {self.openrouter_api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/igorvaryvoda/fpv-caption-creator",
            "X-Title": "FPV Caption Creator"
        }

        data = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": prompts[platform]
                }
            ],
            "max_tokens": 600,
            "temperature": 0.8
        }

        try:
            response = requests.post(self.base_url, headers=headers, json=data)
            response.raise_for_status()

            result = response.json()
            return result['choices'][0]['message']['content'].strip()

        except requests.exceptions.RequestException as e:
            st.error(f"❌ Error generating caption: {str(e)}")
            return None
        except (KeyError, IndexError) as e:
            st.error(f"❌ Error parsing response: {str(e)}")
            return None

    def generate_hashtags(self, location, description, platform, model):
        """Generate relevant hashtags"""
        if not self.openrouter_api_key:
            return []

        prompt = f"""
        Generate 10-15 relevant hashtags for an FPV drone video for {platform}:
        Location: {location}
        Flight description: {description}

        Requirements:
        - Mix of popular and niche hashtags
        - Include location-based hashtags if applicable
        - Include FPV and drone-related hashtags
        - Make them relevant to the content
        - No explanations, just return hashtags separated by spaces

        Format: #hashtag1 #hashtag2 #hashtag3 etc.
        """

        headers = {
            "Authorization": f"Bearer {self.openrouter_api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/igorvaryvoda/fpv-caption-creator",
            "X-Title": "FPV Caption Creator"
        }

        data = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 800,
            "temperature": 0.8
        }

        try:
            response = requests.post(self.base_url, headers=headers, json=data)
            response.raise_for_status()

            result = response.json()
            hashtags_text = result['choices'][0]['message']['content'].strip()

            # Extract hashtags from the response
            hashtags = [tag.strip() for tag in hashtags_text.split() if tag.startswith('#')]
            return hashtags

        except requests.exceptions.HTTPError as e:
            if response.status_code == 400:
                try:
                    error_detail = response.json()
                    st.warning(f"⚠️ API Error: {error_detail.get('error', {}).get('message', 'Bad request')}")
                except:
                    st.warning(f"⚠️ Could not generate hashtags: HTTP 400 - Check your API key and model availability")
            else:
                st.warning(f"⚠️ Could not generate hashtags: HTTP {response.status_code}")
            return []
        except Exception as e:
            st.warning(f"⚠️ Could not generate hashtags: {str(e)}")
            return []

def main():
    st.markdown('<h1 class="main-header">🚁 FPV Caption Creator</h1>', unsafe_allow_html=True)
    st.markdown("### Transform your FPV flights into engaging social media content!")

    # Initialize the generator
    generator = FPVCaptionGenerator()

    # Sidebar for inputs
    with st.sidebar:
        st.header("📝 Flight Details")

        location = st.text_input(
            "📍 Location",
            placeholder="e.g., Sunset Beach, California",
            help="Where did you fly? Be specific for better results!"
        )

        description = st.text_area(
            "✈️ Flight Description",
            placeholder="e.g., High-speed chase through narrow canyon walls, diving under bridges, sunrise golden hour lighting",
            help="Describe what makes this flight special - speed, maneuvers, scenery, lighting, etc.",
            height=120
        )

        st.header("🤖 AI Model Selection")
        model_options = [
            "google/gemini-2.5-flash-lite-preview-06-17",
            "meta-llama/llama-4-maverick",
            "openai/gpt-4.1-mini",
            "google/gemini-2.5-flash",
            "google/gemini-2.0-flash-001",
            "deepseek/deepseek-r1-0528",
            "anthropic/claude-sonnet-4",
            "openrouter/cypher-alpha:free",
            "deepseek/deepseek-chat-v3-0324:free",
        ]

        selected_model = st.selectbox(
            "Choose AI model:",
            options=model_options,
            index=0,  # Default to gemini-2.5-flash-lite-preview-06-17
            help="Select which AI model to use for generating captions and hashtags"
        )

        st.header("🎯 Platform Selection")
        platforms = st.multiselect(
            "Choose platforms:",
            ["Instagram", "TikTok", "YouTube Shorts"],
            default=["Instagram"],
            help="Select which platforms you want captions for"
        )

        generate_button = st.button("🚀 Generate Captions", type="primary")

    # Main content area
    if generate_button:
        if not location or not description:
            st.error("⚠️ Please fill in both location and flight description!")
            return

        if not platforms:
            st.error("⚠️ Please select at least one platform!")
            return

        # Show loading spinner
        with st.spinner("🤖 Generating your epic captions..."):

            # Generate captions for each platform
            for platform in platforms:
                platform_key = platform.lower().replace(" ", "_")

                # Platform-specific icons
                platform_icons = {
                    "Instagram": "📸",
                    "TikTok": "🎵",
                    "YouTube Shorts": "📺"
                }

                # Create platform card
                st.markdown(f'<div class="platform-header">{platform_icons.get(platform, "📱")} {platform}</div>', unsafe_allow_html=True)

                # Generate caption
                caption = generator.generate_caption(location, description, platform_key, selected_model)

                if caption:
                    if platform == "YouTube Shorts" and "TITLE:" in caption and "DESCRIPTION:" in caption:
                        # Parse YouTube Shorts format
                        parts = caption.split("DESCRIPTION:")
                        title = parts[0].replace("TITLE:", "").strip()
                        desc = parts[1].strip()

                        st.markdown("**📺 Title:**")
                        st.code(title, language="text")

                        st.markdown("**📝 Description:**")
                        st.code(desc, language="text")
                    else:
                        st.markdown("**📝 Caption:**")
                        st.code(caption, language="text")

                    # Generate hashtags
                    hashtags = generator.generate_hashtags(location, description, platform_key, selected_model)

                    if hashtags:
                        st.markdown("**#️⃣ Suggested Hashtags:**")
                        hashtag_text = " ".join(hashtags)
                        st.code(hashtag_text, language="text")

                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown("---")

    # Instructions and tips
    with st.expander("💡 Tips for Better Results"):
        st.markdown("""
        **Location Tips:**
        - Be specific: "Malibu Beach, California" vs "beach"
        - Include landmarks: "Golden Gate Bridge, San Francisco"
        - Mention unique features: "Red rock formations, Sedona"

        **Description Tips:**
        - Include flight style: "smooth cinematic" vs "aggressive racing"
        - Mention lighting: "golden hour", "blue hour", "overcast"
        - Describe maneuvers: "power loops", "knife edge", "gap shots"
        - Add emotions: "heart-pounding", "peaceful", "adrenaline rush"

        **Platform Guidelines:**
        - **Instagram**: Focus on visual storytelling and engagement
        - **TikTok**: Keep it short, trendy, and shareable
        - **YouTube Shorts**: Optimize for search and discovery
        """)

    # Footer
    st.markdown("---")
    st.markdown("Made with ❤️ for the FPV community | Powered by Gemini AI")

if __name__ == "__main__":
    main()