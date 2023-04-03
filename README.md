
<h1 align="center">
  <br>
  <a href="https://github.com/EdenX-97/chat-tools"><img src="https://raw.githubusercontent.com/EdenX-97/chat-tools/main/assets/logo.png" alt="chattools" width="200"></a>
  <br>
  Chat Tools
  <br>
</h1>

<h4 align="center">Enhanced GPT with more features and faster speed</h4>

<p align="center">
  <a href="https://github.com/EdenX-97/chat-tools">
      <img src="https://img.shields.io/github/last-commit/EdenX-97/chat-tools">
  </a>
  <a href="https://www.gnu.org/licenses/gpl-3.0.en.html">
      <img src="https://img.shields.io/github/license/EdenX-97/chat-tools">
  </a>
  <a href="https://github.com/EdenX-97/chat-tools">
      <img src="https://img.shields.io/github/stars/EdenX-97/chat-tools?style=social">
  </a>
</p>

![screenshot](https://raw.githubusercontent.com/EdenX-97/chat-tools/main/assets/chat-tools.gif)

## Key Features

- Based on gpt-api
- Faster response
- Automatic summarization
- Save chat history
- Predefined tools (most from [awesome-chatgpt-prompts](https://github.com/f/awesome-chatgpt-prompts))
- Online search
- Documents search

## How To Install

### Download

To clone and run this application, you'll need [Git](https://git-scm.com), [Python](https://www.python.org/downloads/) (Suggest version 3.9.0+) and [Firefox - ESR](https://www.mozilla.org/en-US/firefox/enterprise/#download) installed on your computer. From your command line:

```bash
# Clone this repository
$ git clone https://github.com/EdenX-97/chat-tools

# Go into the repository
$ cd chat-tools

# Install dependencies
$ pip3 install -r requirements.txt
```


### Set up

You have 3 ways to set up the [OpenAI API Key](https://platform.openai.com/account/api-keys):

1. Create a file named `openai_api_key.txt` in the root directory and paste your api-key in it.
2. Run the app, enable professional mode and paste your api-key in the input space.
3. If you use [Hugging Face](https://huggingface.co/), you can set up your api-key in your *Space - Settings - Repository secrets - New secret*
    - Name: OPENAI_API_KEY
    - Secret value: your openai api key

### Run

```bash
# Run the app
$ python3 app.py
```

## Related

[Gradio](https://github.com/gradio-app/gradio) - Awsome python web app framework

[ChuanhuChatGPT](https://github.com/GaiZhenbiao/ChuanhuChatGPT) - Provided valuable inspiration

## Support

<a href="https://www.buymeacoffee.com/edenxu97" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>

<!-- ## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=EdenX-97/chat-tools&type=Date)](https://star-history.com/#EdenX-97/chat-tools&Date) -->

## License

Licensed under the [GPL-3.0](https://www.gnu.org/licenses/gpl-3.0.en.html) license.
