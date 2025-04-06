
import streamlit as st
import requests
import json
import re


def get_chat_response(catalog_file, manifest_file, node_to_parse, prompt):
    url = 'http://fastapi:8080/get_node_in_english'
    with requests.post(
            url,
            stream=True,
            files={'catalog_file': catalog_file,
                   'manifest_file': manifest_file},
            data={'node_to_parse': node_to_parse,
                  'prompt': prompt}
            ) as response:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                parsed_chunk = str(chunk, encoding="utf-8")
                yield parsed_chunk


with st.form("user_form"):
    catalog_file = st.file_uploader("Upload Catalog",
                                    type=['json'])
    manifest_file = st.file_uploader("Upload Manifest",
                                     type=["json"])
    with open('streamlit/default_prompt.txt', 'r') as f:
        default_prompt = f.read()
    prompt = st.text_area("System Prompt",
                          value=default_prompt,
                          height=200)
    nodes_to_parse = []
    if manifest_file:
        json_data = json.load(manifest_file)
        keys = list(json_data['nodes'].keys())
        nodes_to_parse = st.multiselect("Select a node id",
                                        [key for key in keys
                                         if key.split('.')[0] == 'model'])
        manifest_file.seek(0)
    submitted = st.form_submit_button("Parse Json Files" if not manifest_file
                                      else "Submit")

if submitted:
    if catalog_file and manifest_file and nodes_to_parse:
        for node_to_parse in nodes_to_parse:
            with st.expander(node_to_parse):
                response = st.write_stream(get_chat_response(catalog_file, manifest_file,
                                                             node_to_parse, prompt))
                # graph_td = response[response.find('graph TD'):]
                match = re.search(r'graph TD.*?(?=```|$)', response, re.DOTALL)
                graph_td = match.group(0) if match else None
                html_code = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <script type="module">
                        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
                        mermaid.initialize({{ startOnLoad: true }});
                    </script>
                    <script src="https://cdn.jsdelivr.net/npm/panzoom@9.4.0/dist/panzoom.min.js"></script>
                    <style>
                        #mermaid-container {{
                            width: 100%;
                            height: 100%;
                            overflow: hidden;
                            border: 1px solid #ccc;
                        }}
                        #mermaid-zoom {{
                            width: 100%;
                            height: 100%;
                        }}
                    </style>
                </head>
                <body>
                    <div id="mermaid-container">
                        <div id="mermaid-zoom">
                            <div class="mermaid">
                                {graph_td}
                            </div>
                        </div>
                    </div>
                    <script>
                        const zoomElement = document.getElementById('mermaid-zoom');
                        panzoom(zoomElement, {{
                            zoomSpeed: 0.065,
                            maxZoom: 5,
                            minZoom: 0.5
                        }});
                    </script>
                </body>
                </html>
                """
                st.components.v1.html(html_code, height=300)
                manifest_file.seek(0)
                catalog_file.seek(0)
    else:
        st.warning("Please upload files before submitting and add node id.")
