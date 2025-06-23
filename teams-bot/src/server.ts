import express from 'express';
import { BotFrameworkAdapter, TurnContext } from 'botbuilder';
import axios from 'axios';
import dotenv from 'dotenv';

interface PythonResponse {
    response: string;
}

// Load environment variables
dotenv.config();

const app = express();
const port = process.env.PORT || 3978;

// Create bot adapter
const adapter = new BotFrameworkAdapter({
    appId: process.env.MICROSOFT_APP_ID || '',
    appPassword: process.env.MICROSOFT_APP_PASSWORD || ''
});

// Add error handler
adapter.onTurnError = async (context, error) => {
    console.error(`\n [onTurnError] unhandled error: ${error}`);
    await context.sendActivity('Sorry, it looks like something went wrong!');
};

// Parse incoming requests
app.use(express.json());

// Listen for incoming requests
app.post('/api/messages', (req, res) => {
    adapter.processActivity(req, res, async (context) => {
        await onTurn(context);
    });
});

// Handle bot logic
async function onTurn(context: TurnContext) {
    if (context.activity.type === 'message') {
        const userMessage = context.activity.text;
        console.log(`Received message: ${userMessage}`);
        
        try {
            // Call your Python backend
            const response = await axios.post<PythonResponse>('http://localhost:8000/query', {
                message: userMessage
            });
            
            const botResponse = response.data.response;
            await context.sendActivity(botResponse);
            
        } catch (error) {
            console.error('Error calling Python backend:', error);
            await context.sendActivity('Sorry, I encountered an error processing your request.');
        }
    }
}

app.listen(port, () => {
    console.log(`Teams bot is running on port ${port}`);
});