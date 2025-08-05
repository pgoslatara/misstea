# Miss Tea

Ah, go on, go on, go on! Welcome to Miss Tea, your friendly AI assistant, inspired by the one and only Mrs. Doyle. She's here to help you with all your coding needs, and she won't take no for an answer!

<div style="text-align: center;">
    <img src="./images/mrs_doyle.png" align="center" alt="Description of your image" width="50%" height="auto">
</div>

## Requirements

Before you can have a nice cup of tea (or run this project), you'll need a few things:

* **Python 3.12**: Like a good cup of tea, this project requires a solid base.
* **uv**: For managing the Python environment. It's like the sugar that makes everything sweet.
* **A Google AI Studio API key**: To get the AI magic working. Get one [here](https://aistudio.google.com/app/apikey).

## Quickstart Guide

Here's how to get started with Miss Tea in a jiffy:

1. **Clone the repository:**
    ```bash
    git clone https://github.com/pgoslatara/misstea.git
    cd misstea
    ```

1. **Install dependencies:**
    ```bash
    make install
    ```

1. **Set up your environment:**
    Create a `.env` file in the root of the project and add the necessary environment variables:
    ```bash
    export GOOGLE_API_KEY=<TOKEN>
    export MY_EMAIL_ADDRESS=<YOUR_EMAIL_ADDRESS>

    # Only required if using the GitHub subagent
    export PERSONAL_ACCESS_TOKEN_GITHUB=<TOKEN>

    # Only required if using the Outlook subagent
    export MICROSOFT_CLIENT_ID=<TOKEN>
    export MICROSOFT_CLIENT_SECRET=<TOKEN>
    export TENANT_ID=<TOKEN>
    ```

1. **Run the agent:**
    ```bash
    misstea
    ```

Now you're all set! Go on, give it a try!

## Development

If you'd like to contribute to Miss Tea, here's how you can get set up for development:

1. **Follow the Quickstart Guide** to get the basics set up.

1. **Install pre-commit**:
    ```bash
    pre-commit install
    ```

1. **Run the tests:**
    Before you make any changes, make sure the tests are passing:
    ```bash
    make test
    ```

1. **Make your changes:**
    Now you're ready to make your changes. Go on, you will, you will, you will!

---

Ah, you're still here! That's grand. If you have any questions, don't be shy. Go on, ask away!
