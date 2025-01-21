# zoleo-openai-interface
A python script that allows you to communicate with openAI models from your zoleo device.  
Sometimes you are in a remote area where you do not have internet access, deploy this script to ask chatGPT a question from anywhere via email!
## How to Use
***As of now, all these instructions are for Gmail accounts.  If you have a different email provider and cannot get this to work message me here on github, I would be glad to help you.***  
In order to access your emails from a python script, you will need to have an App Password.
* Make sure 2-step authorization is enabled for your email address
* Once you have 2-step authorization enabled, get your [app password](https://myaccount.google.com/apppasswords)
  
Now that you set up your app password, you will need to set an environment variable to your app password and an environment variable for your email address.  How you go about this will depend on where you deploy your app, but the variable names *must* be **EMAIL** and **PASSWORD** spelled exactly like that.  This is because I gave them those names in my script.  You might need to assign them in a bash-script or `.bashrc` file like this
```
EMAIL='Your-email-address'
PASSWORD='your-app-password'
```

Lastly, you will need to have an openAI account and you will need to pay those greedy bastards in order to use a model.  [This link](https://www.datacamp.com/tutorial/using-gpt-models-via-the-openai-api-in-python) should help with that.  

