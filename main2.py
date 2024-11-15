import streamlit as st
from pathlib import Path
import tempfile
from cleaner1 import cleaner  # Our new cleaner
import json
from datetime import datetime
import time

st.set_page_config(
    page_title="Content Cleaner",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced UI styling
st.markdown("""
    <style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
    }
    .element-container {
        margin-bottom: 1rem;
    }
    .stMarkdown p {
        margin-bottom: 0.5rem;
    }
    .stButton button {
        width: 100%;
    }
    .css-1v0mbdj.etr89bj1 {
        width: 100%;
    }
    .stats-card {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8f9fa;
        margin-bottom: 1rem;
    }
    .clean-header {
        color: #1f2937;
        margin-bottom: 1rem;
    }
    /* Dark mode compatible styles */
    @media (prefers-color-scheme: dark) {
        .stats-card {
            background-color: #1f2937;
        }
        .clean-header {
            color: #f3f4f6;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def format_timestamp(dt_str):
    """Format ISO timestamp to readable format"""
    dt = datetime.fromisoformat(dt_str)
    return dt.strftime("%B %d, %Y %H:%M:%S")

def show_stats_cards(stats):
    """Display enhanced statistics cards"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="stats-card">
                <h3>Cleaning Stats</h3>
                <p>Patterns Removed: {}</p>
                <p>Size Reduction: {}%</p>
            </div>
        """.format(
            stats['patterns_removed'],
            round((1 - stats['final_length']/stats['original_length']) * 100, 1)
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="stats-card">
                <h3>Content Structure</h3>
                <p>Headers: {}</p>
                <p>Code Blocks: {}</p>
                <p>Lists: {}</p>
            </div>
        """.format(
            stats['headers'],
            stats['code_blocks'],
            stats['lists']
        ), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="stats-card">
                <h3>Document Stats</h3>
                <p>Original Length: {:,}</p>
                <p>Final Length: {:,}</p>
            </div>
        """.format(
            stats['original_length'],
            stats['final_length']
        ), unsafe_allow_html=True)

def main():
    # Sidebar for history
    with st.sidebar:
        st.title("Processing History")
        if 'history' not in st.session_state:
            st.session_state.history = []
        
        for idx, item in enumerate(st.session_state.history):
            with st.expander(f"Document {idx + 1} - {format_timestamp(item['timestamp'])}"):
                st.json(item['stats'])
                if st.button(f"Restore {idx + 1}", key=f"restore_{idx}"):
                    st.session_state.result = item['result']
                    st.experimental_rerun()

    # Main content
    col1, col2 = st.columns([2, 3])
    
    with col1:
        st.title("Content Cleaner")
        st.markdown("""
        Transform messy content into clean, formatted markdown.
        Automatically removes noise and enhances readability.
        """)
        
        # Input method tabs
        tab1, tab2 = st.tabs(["📄 Upload PDF", "✍️ Paste Text"])
        
        with tab1:
            uploaded_file = st.file_uploader(
                "Drop your PDF here",
                type=['pdf'],
                help="Maximum size: 50MB"
            )
            
            if uploaded_file:
                with st.spinner("Processing PDF..."):
                    # Save uploaded file temporarily
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_path = Path(tmp_file.name)
                    
                    # Process PDF
                    try:
                        result = cleaner.clean_pdf(tmp_path)
                        tmp_path.unlink()  # Clean up
                        
                        # Add to history
                        st.session_state.history.append({
                            'timestamp': datetime.now().isoformat(),
                            'stats': result['metadata']['stats'],
                            'result': result
                        })
                        
                        st.session_state.result = result
                        st.success("PDF processed successfully!")
                        st.balloons()
                    except Exception as e:
                        st.error(f"Error processing PDF: {str(e)}")
        
        with tab2:
            text_input = st.text_area(
                "Paste your text here",
                height=300,
                help="Paste any text content to clean and format"
            )
            
            if text_input:
                with st.spinner("Cleaning text..."):
                    result = cleaner.clean_text(text_input)
                    
                    # Add to history
                    st.session_state.history.append({
                        'timestamp': datetime.now().isoformat(),
                        'stats': result['metadata']['stats'],
                        'result': result
                    })
                    
                    st.session_state.result = result
                    st.success("Text cleaned successfully!")
                    st.balloons()

        # Show cleaning capabilities
        with st.expander("🔍 View Cleaning Capabilities"):
            st.markdown("""
            **Removes:**
            - Headers and footers
            - Page numbers
            - Contact information
            - URLs and email addresses
            - Institutional boilerplate
            - Formatting artifacts
            
            **Enhances:**
            - Detects and formats headers
            - Preserves code blocks
            - Formats lists consistently
            - Maintains document structure
            - Improves readability
            """)
    
    with col2:
        if 'result' in st.session_state:
            result = st.session_state.result
            
            # Enhanced stats display
            show_stats_cards(result['metadata']['stats'])
            
            # Content tabs
            tab1, tab2, tab3 = st.tabs(["🔄 Live Rebuild", "🔍 Compare", "📊 Details"])
            
            with tab1:
                st.markdown("### Watching the Markdown Build")
                
                # Create containers for each section
                title_container = st.empty()
                authors_container = st.empty()
                abstract_container = st.empty()
                content_container = st.empty()
                
                # Split content into sections
                lines = result['text'].split('\n')
                current_section = []
                built_markdown = ""
                
                for line in lines:
                    time.sleep(0.1)  # Small delay for visual effect
                    
                    # Handle different section types
                    if line.startswith('# '):  # Title
                        title_container.markdown(line)
                        continue
                    
                    elif line.startswith('*'):  # Authors/Affiliations
                        authors_container.markdown(line)
                        continue
                    
                    elif line.startswith('## Abstract'):
                        abstract_container.markdown("\n".join(current_section))
                        current_section = [line]
                        continue
                    
                    current_section.append(line)
                    built_markdown = "\n".join(current_section)
                    content_container.markdown(built_markdown)
                
                # Add download options after completion
                st.success("✨ Document rebuild complete!")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.download_button(
                        "📥 Download Markdown",
                        result['text'],
                        file_name=f"cleaned_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                        mime="text/markdown"
                    )
                with col2:
                    st.download_button(
                        "📥 Download Text",
                        result['text'],
                        file_name=f"cleaned_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain"
                    )
                with col3:
                    st.download_button(
                        "📥 Download JSON",
                        json.dumps(result, indent=2),
                        file_name=f"cleaned_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
            
            with tab2:
                col_left, col_right = st.columns(2)
                with col_left:
                    st.markdown("##### Original")
                    st.text_area(
                        label="Original Text",
                        value=result['metadata']['original_text'],
                        height=400,
                        key="original_view",
                        label_visibility="collapsed"
                    )
                with col_right:
                    st.markdown("##### Cleaned")
                    st.text_area(
                        label="Cleaned Text",
                        value=result['text'],
                        height=400,
                        key="cleaned_view",
                        label_visibility="collapsed"
                    )
            
            with tab3:
                st.json(result['metadata'])

if __name__ == "__main__":
    main()