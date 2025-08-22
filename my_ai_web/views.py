from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import google.generativeai as genai
import os
import logging
from .models import ChatMessage
from django.core.serializers import serialize
import json

# Set up logging
logger = logging.getLogger(__name__)

# Configure Google AI with your API key
genai.configure(api_key="AIzaSyAx_FIJo5OObJdg4aiNeHxfutPbHraZomE")

def chat_page(request):
    return render(request, "chat.html")

@csrf_exempt
def test_api(request):
    """Simple test endpoint to verify API is working"""
    return JsonResponse({"status": "success", "message": "API is working!"})

@csrf_exempt
def get_chat_history(request):
    """Get all chat history"""
    try:
        messages = ChatMessage.objects.all()[:50]  # Get last 50 messages
        history = []
        for msg in messages:
            history.append({
                'user_message': msg.user_message,
                'ai_response': msg.ai_response,
                'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            })
        return JsonResponse({"history": history})
    except Exception as e:
        logger.error(f"Error loading chat history: {e}")
        return JsonResponse({"history": []})

@csrf_exempt
def clear_chat_history(request):
    """Clear all chat history"""
    try:
        ChatMessage.objects.all().delete()
        return JsonResponse({"status": "success", "message": "Chat history cleared"})
    except Exception as e:
        logger.error(f"Error clearing chat history: {e}")
        return JsonResponse({"status": "error", "message": str(e)})

@csrf_exempt
def get_response(request):
    try:
        if request.method == "GET":
            user_input = request.GET.get("message", "")
            if not user_input:
                return JsonResponse({"response": "Please type something!"})

            logger.info(f"Processing request for message: {user_input}")
            
            try:
                # Use Google's Generative AI model - try different model names
                try:
                    # Try gemini-1.5-flash first (newer model)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content(user_input)
                    reply = response.text
                except:
                    try:
                        # Try gemini-1.5-pro
                        model = genai.GenerativeModel('gemini-1.5-pro')
                        response = model.generate_content(user_input)
                        reply = response.text
                    except:
                        # Try gemini-pro
                        model = genai.GenerativeModel('gemini-pro')
                        response = model.generate_content(user_input)
                        reply = response.text
                
                # Ensure proper formatting for markdown rendering
                if reply:
                    # Clean up the response for better markdown rendering
                    reply = reply.strip()
                    # Ensure proper line breaks for lists and sections
                    reply = reply.replace('\n\n', '\n').replace('\n\n\n', '\n\n')
                
                # Save the conversation to database
                try:
                    chat_message = ChatMessage.objects.create(
                        user_message=user_input,
                        ai_response=reply
                    )
                    logger.info(f"Saved chat message with ID: {chat_message.id}")
                except Exception as save_error:
                    logger.error(f"Error saving chat message: {save_error}")
                
                logger.info(f"Successfully got response: {reply[:100]}...")
                return JsonResponse({"response": reply})
                
            except Exception as api_error:
                logger.error(f"Google AI API error: {api_error}")
                return JsonResponse({"response": f"AI service error: {str(api_error)}"})
        
        return JsonResponse({"response": "Invalid request method"})
        
    except Exception as e:
        logger.error(f"Unexpected error in get_response: {e}")
        return JsonResponse({"response": f"Server error: {str(e)}"})