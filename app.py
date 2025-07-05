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
        background: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #4ecdc4;
    }

    .hashtag-section {
        background: #e8f4f8;
        padding: 1rem;
        border-radius: 8px;
        margin-top: 1rem;
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
</style>
""", unsafe_allow_html=True)

class FPVCaptionGenerator:
    def __init__(self):
        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"

    def generate_caption(self, location, description, platform):
        """Generate caption using Gemini via OpenRouter"""
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

            Format: Just return the caption text, no extra formatting.
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

            Format: Just return the caption text, no extra formatting.
            """,

            "youtube_shorts": f"""
            Create both a title and description for a YouTube Shorts FPV drone video:
            Location: {location}
            Flight description: {description}

            Requirements:
            - Title: Under 60 characters, clickable and SEO-friendly
            - Description: Under 125 words, informative but engaging
            - Include relevant keywords for discoverability

            Format:
            TITLE: [your title here]
            DESCRIPTION: [your description here]
            """
        }

        headers = {
            "Authorization": f"Bearer {self.openrouter_api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "google/gemini-2.5-flash-lite-preview-06-17",
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

    def generate_hashtags(self, location, description, platform):
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
            "Content-Type": "application/json"
        }

        data = {
            "model": "google/gemini-pro",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 200,
            "temperature": 0.6
        }

        try:
            response = requests.post(self.base_url, headers=headers, json=data)
            response.raise_for_status()

            result = response.json()
            hashtags_text = result['choices'][0]['message']['content'].strip()

            # Extract hashtags from the response
            hashtags = [tag.strip() for tag in hashtags_text.split() if tag.startswith('#')]
            return hashtags

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

                st.markdown(f'<div class="platform-card">', unsafe_allow_html=True)
                st.subheader(f"📱 {platform}")

                # Generate caption
                caption = generator.generate_caption(location, description, platform_key)

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
                    hashtags = generator.generate_hashtags(location, description, platform_key)

                    if hashtags:
                        st.markdown('<div class="hashtag-section">', unsafe_allow_html=True)
                        st.markdown("**#️⃣ Suggested Hashtags:**")
                        hashtag_text = " ".join(hashtags)
                        st.code(hashtag_text, language="text")
                        st.markdown('</div>', unsafe_allow_html=True)

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