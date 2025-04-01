from langchain_aws import ChatBedrock


class DbtToEnglish:
    def __init__(self, dbt_manifest, dbt_catalog, node_id, prompt):
        self._llm = None
        self.dbt_manifest = dbt_manifest
        self.dbt_catalog = dbt_catalog
        self.node_id = node_id
        self._system_message = None
        self.custom_prompt = prompt
        self.max_level = 2
        self._messages = None

    @property
    def messages(self):
        self._messages = [
            ('system', self.custom_prompt),
        ]
        return self._messages

    @property
    def llm(self):
        self._llm = ChatBedrock(
            model_id='anthropic.claude-3-5-sonnet-20240620-v1:0',
            model_kwargs=dict(temperature=0, max_tokens=4096,),
        )
        return self._llm

    @staticmethod
    def upload_dbt_node(node, dbt_manifest, dbt_catalog, prompt):
        return DbtToEnglish(dbt_manifest=dbt_manifest,
                            dbt_catalog=dbt_catalog,
                            node_id=node,
                            prompt=prompt).get_model_explanation()

    @staticmethod
    def get_dict_type_for_manifest(type_name):
        dict_type = 'nodes'
        if type_name == 'source':
            dict_type = 'sources'
        return dict_type

    @staticmethod
    def parse_artifacts_dict(artifacts_dict):
        parsed_dict = {
            'database': artifacts_dict.get('database'),
            'schema': artifacts_dict.get('schema'),
            'model_name': artifacts_dict.get('name'),
            'resource_type': artifacts_dict.get('resource_type'),
            'alias': artifacts_dict.get('alias'),
            'meta': artifacts_dict.get('config', {}).get('meta'),
            'materialized': artifacts_dict.get('config', {})
            .get('materialized'),
            'grants': artifacts_dict.get('config', {}).get('grants'),
            'description': artifacts_dict.get('description', {}),
            'raw_code': artifacts_dict.get('raw_code', {}),
            'depends_on': artifacts_dict.get('depends_on', {}),
            'columns': artifacts_dict.get('catalog_dict', {}).get('columns'),
            'rows_number': artifacts_dict.get('catalog_dict', {}).get('stats',
                                                                      {})
            .get('rows', {}).get('value')
        }
        return parsed_dict

    def get_model_explanation_from_llm(self, metadata_list):
        for chunk in self.llm.stream(self.messages +
                                     [('human',
                                      f"""Tell me about {self.node_id} model.
                                    {metadata_list}""")]):
            yield chunk.content

    def get_dbt_manifest_list(self):
        metadata_list = []

        def get_dependencies(node_id, level=1):
            type_name = node_id.split('.')[0]
            dict_type = DbtToEnglish.get_dict_type_for_manifest(type_name)
            main_dict = self.dbt_manifest[dict_type].get(node_id, None)
            if not main_dict:
                return
            main_dict['catalog_dict'] = self.dbt_catalog[dict_type]\
                .get(node_id, {})
            if level <= self.max_level or type_name == 'source':
                if level > 1:
                    # main_dict['raw_code'] = None
                    main_dict['catalog_dict'] = {}
                metadata_list.append(DbtToEnglish.parse_artifacts_dict(
                    main_dict))
            for dep in main_dict.get('depends_on', {}).get('nodes', []):
                get_dependencies(dep, level+1)
        get_dependencies(self.node_id)
        return metadata_list

    def get_model_explanation(self):
        metadata_list = self.get_dbt_manifest_list()
        return self.get_model_explanation_from_llm(metadata_list)
