try:
    from ibm_watsonx_ai.foundation_models import Model
    print("✅ IBM watsonx.ai SDK installed successfully")
except ImportError as e:
    print("❌ IBM watsonx.ai SDK not installed")
    print(f"Error: {e}")

# Made with Bob
