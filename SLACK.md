# Slack Setup

1. Nagivate to https://api.slack.com/apps and **Create new app** > **From scratch**. Give it a Name & Workspace

    ![Slack Setup 01](img/slack-setup-01.jpg)

2. **Basic information** > **Add features & functionality** > **Slash commands**

    ![Slack Setup 02](img/slack-setup-02.jpg)

3. Retrieve the following environment variables for use in the Lambda

    * `SLACK_SIGNING_SECRET`: **Basic information** > **App credentials**
    * `SLACK_BOT_TOKEN`: **OAuth & Permissions** > starts with `xoxo-`

4. Create secret

    ```bash
    aws secretsmanager create-secret \
        --name slackbot-wordle \
        --secret-string "{\"signing\":\"xxxxxxxxx\",\"token\": \"xoxb-xxxx\"\}"
    ```
