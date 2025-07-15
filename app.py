from typing import Optional, Tuple
import gradio as gr
from threading import Lock
from langchain.chains.conversation.base import ConversationChain
from langchain_community.chat_models import ChatZhipuAI
from langchain_community.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory


class LLMEngine:
    @staticmethod
    def get_model(engine: str, api_key: str = None):
        engine = engine.lower()

        if engine == "openai":
            return ChatOpenAI(
                temperature=0.7
            )

        elif engine == "zhipu":
            return ChatZhipuAI(
                api_key=api_key,
                model="glm-4-flash-250414"
            )

        elif engine == "claude":
            raise NotImplementedError("Claude 接入未实现")

        else:
            raise ValueError(f"Unsupported engine: {engine}")


class APIManager:

    def __init__(self, engine: str = "OpenAI", api_key: str = None):
        self.engine = engine
        self.api_key = api_key
        self.llm = None
        self.chain = None

    def load_llm(self):
        self.llm = LLMEngine.get_model(self.engine, self.api_key)
        return self.llm

    def load_chain(self):

        if not self.llm:
            self.load_llm()
        memory = ConversationBufferMemory()
        self.chain = ConversationChain(llm=self.llm, memory=memory, verbose=True)
        return self.chain

    def set_api_key(self, api_key: str):
        self.api_key = api_key
        self.load_llm()
        return self.load_chain()


class ChatWrapper:

    def __init__(self):
        self.lock = Lock()
    def __call__(
            self, inp: str, chain: Optional[ConversationChain], history: Optional[Tuple[str, str]]
    ):
        """Execute the chat functionality."""
        self.lock.acquire()
        try:
            history = history or []
            # If chain is None, that is because no API key was provided.
            if chain is None:
                history.append((inp, "Please paste your ai key to use"))
                return history, history

            # Run chain and append input.
            output = chain.run(input=inp)
            history.append((inp, output))
        except Exception as e:
            raise e
        finally:
            self.lock.release()
        return history, history

chat = ChatWrapper()



engine: dict[str, int] = {
    "Google": 0,
    "Bing": 0,
    "DeepL": 0,
    "DeepLX": 0,
    "Xinference": 0,
    "AzureOpenAI": 0,
    "OpenAI": 0,
    "Zhipu": 0,
    "ModelScope": 0,
    "Silicon": 0,
    "Gemini": 0,
    "Azure": 0,
    "Tencent": 0,
    "Dify": 0,
    "AnythingLLM": 0,
    "Argos Translate": 0,
    "Grok": 0,
    "Groq": 0,
    "DeepSeek": 0,
    "OpenAI-liked": 0,
    "Ali Qwen-Translation": 0,
}




# Global setup
custom_blue = gr.themes.Color(
    c50="#E8F3FF",
    c100="#BEDAFF",
    c200="#94BFFF",
    c300="#6AA1FF",
    c400="#4080FF",
    c500="#165DFF",
    c600="#0E42D2",
    c700="#0A2BA6",
    c800="#061D79",
    c900="#03114D",
    c950="#020B33",
)


custom_css = """
    .secondary-text {color: #999 !important;}
    footer {visibility: hidden}
    .env-warning {color: #dd5500 !important;}
    .env-success {color: #559900 !important;}

    /* Add dashed border to input-file class */
    .input-file {
        border: 1.2px dashed #165DFF !important;
        border-radius: 6px !important;
    }

    .progress-bar-wrap {
        border-radius: 8px !important;
    }

    .progress-bar {
        border-radius: 8px !important;
    }

    .pdf-canvas canvas {
        width: 100%;

    }

    """


env_field_map = {
    "Zhipu": {
        "API Key": "zhipu_key_default"
    },
    "Tencent": {
        "SecretId": "tencent_secret_id_default",
        "SecretKey": "tencent_secret_key_default"
    },
    "OpenAI": {
        "API Key": "openai_api_key",
        "Organization": "openai_org"
    },
    "AzureOpenAI": {
        "API Key": "azure_api_key",
        "Endpoint": "azure_endpoint",
        "Deployment Name": "azure_deployment"
    },
    "Google": {
        "API Key": "google_api_key"
    },
    "Bing": {
        "API Key": "bing_api_key"
    },
    "DeepL": {
        "API Key": "deepl_api_key"
    },
    "DeepLX": {
        "Host URL": "deeplx_url"
    },
    "Xinference": {
        "Base URL": "xinference_base_url"
    },
    "ModelScope": {
        "API Key": "modelscope_key"
    },
    "Silicon": {
        "API Key": "silicon_key"
    },
    "Gemini": {
        "API Key": "gemini_key"
    },
    "Azure": {
        "API Key": "azure_key",
        "Endpoint": "azure_endpoint"
    },
    "Dify": {
        "API Key": "dify_key"
    },
    "AnythingLLM": {
        "API Key": "anythingllm_key"
    },
    "Grok": {
        "API Key": "grok_key"
    },
    "Groq": {
        "API Key": "groq_key"
    },
    "DeepSeek": {
        "API Key": "deepseek_key"
    },
    "OpenAI-liked": {
        "API Key": "openai_like_key"
    },
    "Ali Qwen-Translation": {
        "API Key": "ali_qwen_key"
    }
}


env_config_map = {
    "Zhipu": ["API Key"],
    "Tencent": ["SecretId", "SecretKey"],
    "OpenAI": ["API Key", "Organization"],
    "AzureOpenAI": ["API Key", "Endpoint", "Deployment Name"],
    "Google": ["API Key"],
    "Bing": ["API Key"],
    "DeepL": ["API Key"],
    "DeepLX": ["Host URL"],
    "Xinference": ["Base URL"],
    "ModelScope": ["API Key"],
    "Silicon": ["API Key"],
    "Gemini": ["API Key"],
    "Azure": ["API Key", "Endpoint"],
    "Dify": ["API Key"],
    "AnythingLLM": ["API Key"],
    "Argos Translate": [],
    "Grok": ["API Key"],
    "Groq": ["API Key"],
    "DeepSeek": ["API Key"],
    "OpenAI-liked": ["API Key"],
    "Ali Qwen-Translation": ["API Key"]
}


def toggle_env_fields(selected_service):
    fields = env_config_map.get(selected_service, [])
    outputs = []
    for i in range(3):
        if i < len(fields):
            outputs.append(gr.update(visible=True, label=fields[i], value=""))
        else:
            outputs.append(gr.update(visible=False))
    outputs.append(gr.update(visible=True))
    return outputs


def save_env(service_name, env1, env2, env3, _agent_state):
    fields_map = env_field_map.get(service_name, {})
    config_attrs = list(fields_map.values())
    values = [env1, env2, env3][:len(config_attrs)]

    api_key = values[0] if values else ""

    manager = APIManager(engine=service_name, api_key=api_key)

    try:
        llm = LLMEngine.get_model(service_name, api_key=api_key)
        chain = ConversationChain(llm=llm, memory=ConversationBufferMemory())
    except Exception as e:
        print(f"Error initializing chain for {service_name}:", e)
        chain = None

    return (
        *[gr.update(visible=False) for _ in range(3)],
        gr.update(visible=False),
        chain
    )



block = gr.Blocks(
        title="TranslaTex",
        theme=gr.themes.Default(
            primary_hue=custom_blue, spacing_size="md", radius_size="lg"
        ),
        css=custom_css,
)


with block:
    gr.Markdown("# langchain ai agent demo", elem_id="header", elem_classes="title")

    chatbot = gr.Chatbot(label=" chatBot", height=600)

    with gr.Row():
        message = gr.Textbox(
            placeholder="What's the answer to life, the universe, and everything?",
            lines=2,
            scale=9,
            show_label=False,
        )
        submit = gr.Button(
            value="Send",
            variant="primary",
            scale=1,
            min_width=80,
        )

    gr.Examples(
        examples=[
            "Hi! How's it going?",
            "What should I do tonight?",
            "What's 2 + 2?",
        ],
        inputs=message,
        label="💡 Example Prompts",
    )

    state = gr.State()
    agent_state = gr.State()

    with gr.Row(equal_height=True):

        service = gr.Dropdown(
            choices=list(engine.keys()),
            value=list(engine.keys())[0],
            label="Service"
        )

        envs = [gr.Textbox(visible=False, label=f"ENV {i + 1}") for i in range(3)]

        save_btn = gr.Button("Save Configuration", visible=False)

        service.change(
            fn=toggle_env_fields,
            inputs=service,
            outputs=envs + [save_btn]
        )

        save_btn.click(
            fn=save_env,
            inputs=[service] + envs + [agent_state],
            outputs=envs + [save_btn, agent_state],
        )


    submit.click(chat, inputs=[message, agent_state, state], outputs=[chatbot, state])
    message.submit(chat, inputs=[message, agent_state, state], outputs=[chatbot, state])


block.launch(debug=True)