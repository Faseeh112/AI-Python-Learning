import os
import PyPDF2
import pandas as pd
import docx2txt
from flask import request, jsonify
from werkzeug.utils import secure_filename
from PersonalDiaryforVisualImpared.db import db
from PersonalDiaryforVisualImpared.Model.Attachments import Attachments

# --- AUTOMATIC FOLDER CREATION ---
UPLOAD_FOLDER = os.path.join('uploads', 'attachments')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


class AttachmentsController:

    @staticmethod
    def extract_text(file_path, extension):
        """Extracts text content to be saved in the database 'context' column."""
        text_content = ""
        try:
            if extension == 'docx':
                text_content = docx2txt.process(file_path)

            elif extension == 'txt':
                with open(file_path, 'r', encoding='utf-8') as f:
                    text_content = f.read()

            elif extension == 'pdf':
                with open(file_path, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    for page in reader.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text_content += page_text + " "

            elif extension in ['xlsx', 'xls']:
                df = pd.read_excel(file_path)
                text_content = df.to_string()

        except Exception as e:
            text_content = f"Extraction failed for .{extension}: {str(e)}"

        return text_content.strip()

    @staticmethod
    def upload_attachment():
        # Check if files and form data are present
        if 'file' not in request.files:
            return jsonify({"error": "No file part in request"}), 400

        file = request.files['file']
        user_id = request.form.get("user_id")
        title = request.form.get("title")

        if not all([file, user_id, title]):
            return jsonify({"error": "Missing file, user_id, or title"}), 400

        try:
            # 1. File handling
            filename = secure_filename(file.filename)
            extension = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
            file_path = os.path.join(UPLOAD_FOLDER, filename)

            file.save(file_path)

            # 2. Text Extraction
            extracted_context = AttachmentsController.extract_text(file_path, extension)

            # 3. Save to DB using your Capitalized Model attributes
            new_attachment = Attachments(
                User_id=int(user_id),
                title=title,
                File_name=filename,
                File_type=extension,
                File_path=file_path,
                context=extracted_context,
                Action_type="Upload"
            )

            db.session.add(new_attachment)
            db.session.commit()

            return jsonify({
                "message": f"'{title}' uploaded to Diary successfully",
                "attachment_id": new_attachment.Attac_id,
                "text_preview": extracted_context[:100] + "..."
            }), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def update_attachment(attac_id):
        # 1. Find the existing record
        attachment = Attachments.query.get(attac_id)
        if not attachment:
            return jsonify({"error": "Attachment not found"}), 404

        title = request.form.get("title")
        user_id = request.form.get("user_id")
        file = request.files.get('file')

        try:
            # 2. Update the Title if provided
            if title:
                attachment.title = title

            # 3. Handle File Replacement if a new file is uploaded
            if file and file.filename != '':
                # Delete the old physical file from the 'uploads/attachments' folder
                if os.path.exists(attachment.File_path):
                    os.remove(attachment.File_path)

                # Save the new file
                filename = secure_filename(file.filename)
                extension = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
                new_file_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(new_file_path)

                # Re-extract text for the new file
                new_context = AttachmentsController.extract_text(new_file_path, extension)

                # Update Model attributes
                attachment.File_name = filename
                attachment.File_path = new_file_path
                attachment.File_type = extension
                attachment.context = new_context
                attachment.Action_type = "Update"

            db.session.commit()

            return jsonify({
                "message": f"Attachment '{attachment.title}' updated successfully",
                "attachment_id": attachment.Attac_id
            }), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def delete_attachment(attac_id):
        try:
            # 1. Find the attachment record
            attachment = Attachments.query.get(attac_id)

            if not attachment:
                return jsonify({"error": "Attachment not found"}), 404

            # 2. Get the file path before we delete the database record
            file_path = attachment.File_path

            # 3. Delete from Database
            db.session.delete(attachment)
            db.session.commit()

            # 4. Delete the physical file from the folder
            # We use os.path.exists to prevent the code from crashing if the file was already moved
            if file_path and os.path.exists(file_path):
                os.remove(file_path)

            return jsonify({
                "message": f"Attachment '{attachment.title}' and its file deleted successfully",
                "status": "Success"
            }), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500