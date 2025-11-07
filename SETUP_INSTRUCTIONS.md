# 🚀 Quick Setup Instructions for Quantum Lotto Bot

## ⚠️ IMPORTANT: Enable Privileged Intents

The bot is ready to run, but you need to enable one setting in Discord first:

### Step-by-Step Setup:

1. **Go to Discord Developer Portal**
   - Visit: https://discord.com/developers/applications
   - Find your bot application (or create a new one)

2. **Enable Message Content Intent** ✅
   - Click on your application
   - Go to the **"Bot"** section in the left sidebar
   - Scroll down to **"Privileged Gateway Intents"**
   - Toggle ON: **"Message Content Intent"** ← THIS IS REQUIRED!
   - Click **"Save Changes"** at the bottom

3. **Get Your Bot Token**
   - In the same "Bot" section
   - Click "Reset Token" (or "Copy" if you already have one)
   - Copy the token
   - Add it to Replit Secrets as `DISCORD_TOKEN`
   ✅ You've already done this step!

4. **Invite the Bot to Your Server**
   - Go to **"OAuth2"** → **"URL Generator"** in the left sidebar
   - Under **"Scopes"**, select:
     - ✅ `bot`
     - ✅ `applications.commands`
   - Under **"Bot Permissions"**, select:
     - ✅ Send Messages
     - ✅ Read Messages/View Channels
     - ✅ Read Message History
     - ✅ Embed Links
     - ✅ Use Slash Commands
   - Copy the generated URL at the bottom
   - Open it in your browser and select your server

5. **Start the Bot**
   - The bot will automatically start once the Message Content Intent is enabled
   - Or click "Run" in Replit to restart it manually

---

## 🎮 Using the Bot

Once the bot is online and in your server, use these commands:

- `/pull` - Pull from the Quantum Lotto (costs 1 credit)
- `/status` - View universe instability and leaderboard
- `/stabilize` - Reduce instability (costs 10 credits)
- `/inventory` - View your loot collection

---

## ❓ Troubleshooting

### "Privileged Intents Required" Error
- Make sure you enabled **Message Content Intent** in the Developer Portal
- Click **Save Changes** after enabling it
- Wait a few seconds, then restart the bot

### Commands Not Showing Up
- Wait 1-5 minutes for Discord to sync the commands
- Try typing `/` in your server to see if they appear
- If still not working, kick and re-invite the bot

### Bot Won't Start
- Check that your `DISCORD_TOKEN` is correct in Replit Secrets
- Make sure the token is from the Bot section, not OAuth2
- Regenerate the token if needed

---

## 🎰 Ready to Play!

Once everything is set up, your Quantum Lotto bot will:
- Track every message to increase instability
- Let users pull for random loot with varying rarities
- Trigger dramatic collapse events when chaos peaks
- Provide an exciting gambling experience for your server!

**May the quantum odds be in your favor!** 💠⚛️🌀
