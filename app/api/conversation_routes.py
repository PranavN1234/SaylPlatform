from flask import request, jsonify
import uuid
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.conversation_model import Conversation, Message
from app.models.user_model import User  # Import user model
from app.api import api_blueprint
from app import db


@api_blueprint.route('/conversations', methods=['GET'])
@jwt_required()
def get_user_conversations():
    try:
        # Get the current user's identity from the JWT token
        current_user_email = get_jwt_identity()

        user = User.query.filter_by(email=current_user_email).first()

        if not user:
            return jsonify({"msg": "User not found"}), 404
        
        # Fetch conversations for the user
        conversations = Conversation.query.filter_by(user_id=user.id).order_by(Conversation.created_at.desc()).all()

        # If no conversations exist, create the first conversation with a default message
        if not conversations:
            # Generate a random session_id using UUID
            session_id = f"session_{uuid.uuid4().hex[:8]}"  # Example: 'session_a1b2c3d4'

            # Create a new conversation
            new_conversation = Conversation(session_id=session_id, user_id=user.id)
            db.session.add(new_conversation)
            db.session.commit()

            default_message_content = {
                "role": "assistant",
                "content": {
                    "message": "Welcome! Ask me about cross rulings, HTS codes, or any other query.",
                },
                "intent": "general"
            }

            # Create a default message for the new conversation
            default_message = Message(
                conversation_id=new_conversation.id,
                user_id=user.id,
                messages=[default_message_content]
            )
            db.session.add(default_message)
            db.session.commit()

            # Add the newly created conversation to the response
            conversations = [new_conversation]

        # Format the conversation list to return as JSON
        conversation_list = [{
            'id': conv.id,
            'session_id': conv.session_id,
            'user_id': conv.user_id,
            'created_at': conv.created_at
        } for conv in conversations]

        return jsonify(conversation_list), 200
    
    except Exception as e:
        return jsonify({"msg": str(e)}), 500


@api_blueprint.route('/conversations/<session_id>/messages', methods=['GET'])
@jwt_required()
def get_conversation_messages(session_id):
    try:
        # Get the page number from the query parameter, default to 1 if not provided
        page = request.args.get('page', 1, type=int)

        # Get the current user's identity from the JWT token
        current_user_email = get_jwt_identity()

        user = User.query.filter_by(email=current_user_email).first()
        if not user:
            return jsonify({"msg": "User not found"}), 404

        # Get the conversation by session_id and make sure it belongs to the user
        conversation = Conversation.query.filter_by(session_id=session_id, user_id=user.id).first()
        if not conversation:
            return jsonify({"msg": "Conversation not found"}), 404

        # Paginate the message batches, order by `created_at` in descending order (most recent first)
        messages_query = Message.query.filter_by(conversation_id=conversation.id).order_by(Message.created_at.desc())
        pagination = messages_query.paginate(page=page, per_page=1, error_out=False)

        # Format messages to return as JSON
        messages_list = [{
            'id': msg.id,
            'conversation_id': msg.conversation_id,
            'user_id': msg.user_id,
            'messages': msg.messages,  # This is the JSON batch of messages
            'created_at': msg.created_at
        } for msg in pagination.items]

        # Include pagination metadata
        response = {
            'messages': messages_list,
            'total_pages': pagination.pages,
            'current_page': pagination.page,
            'total_messages': pagination.total
        }

        return jsonify(response), 200
    
    except Exception as e:
        return jsonify({"msg": str(e)}), 500


@api_blueprint.route('/conversations/create', methods=['POST'])
@jwt_required()
def create_new_conversation():
    try:
        # Get the current user's identity from the JWT token
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()

        if not user:
            return jsonify({"msg": "User not found"}), 404

        # Generate a random session_id using UUID
        session_id = f"session_{uuid.uuid4().hex[:8]}"  # Example: 'session_a1b2c3d4'

        # Create a new conversation with the generated session_id
        new_conversation = Conversation(session_id=session_id, user_id=user.id)
        db.session.add(new_conversation)
        db.session.commit()

        # Create a default message for the new conversation
        default_message_content = {
            "role": "assistant",
            "content": {
                "message": "Welcome! Ask me about cross rulings, HTS codes, or any other query.",
            },
            "intent": "general"
        }
        default_message = Message(conversation_id=new_conversation.id, user_id=user.id, messages=default_message_content)
        db.session.add(default_message)
        db.session.commit()

        # Build the response
        response = {
            "id": new_conversation.id,
            "session_id": new_conversation.session_id,
            "last_message": default_message_content  # Set default message as last message
        }

        return jsonify(response), 201

    except Exception as e:
        return jsonify({"msg": str(e)}), 500



@api_blueprint.route('/conversations/<session_id>', methods=['DELETE'])
@jwt_required()
def delete_conversation(session_id):
    try:
        # Get the current user's identity from the JWT token
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()

        if not user:
            return jsonify({"msg": "User not found"}), 404

        # Find the conversation by session_id and user_id
        conversation = Conversation.query.filter_by(session_id=session_id, user_id=user.id).first()

        if not conversation:
            return jsonify({"msg": "Conversation not found"}), 404

        # Delete the conversation and its associated messages
        db.session.delete(conversation)
        db.session.commit()

        return jsonify({"status": "success", "message": "Conversation deleted"}), 200

    except Exception as e:
        return jsonify({"msg": str(e)}), 500