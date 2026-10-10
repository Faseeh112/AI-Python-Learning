from flask import request, jsonify
from PersonalDiaryforVisualImpared.db import db
from PersonalDiaryforVisualImpared.Model.Item_location import Item_location

class ItemLocationController:

    @staticmethod
    def add_location():
        # 1. Capture the JSON data from the request body
        data = request.get_json()

        # 2. Check if data actually exists
        if not data:
            return jsonify({"error": "No JSON payload received"}), 400

        # 3. Extract values from the JSON
        # Note: We match the keys to what we want to send in Postman
        user_id = data.get("user_id")
        item_name = data.get("item")
        category = data.get("Category")
        description = data.get("Description")
        location_text = data.get("Location")

        # 4. Validation: item, Location, and user_id are mandatory
        if not all([user_id, item_name, location_text]):
            return jsonify({
                "error": "Required fields missing",
                "required": ["user_id", "item", "Location"]
            }), 400

        try:
            # 5. Create the record (Matching your Model's attribute casing)
            new_item_loc = Item_location(
                item=item_name,            # Lowercase in your model
                Category=category,         # Capitalized in your model
                Description=description,   # Capitalized in your model
                Location=location_text,    # Capitalized in your model
                User_id=int(user_id)       # Capitalized in your model
            )

            # 6. Save to Database
            db.session.add(new_item_loc)
            db.session.commit()

            return jsonify({
                "status": "Success",
                "message": f"Location for '{item_name}' has been recorded.",
                "Loc_id": new_item_loc.Loc_id
            }), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def update_location(loc_id):
        # 1. Get the JSON data from the request body
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        # 2. Find the existing record using the loc_id from the URL parameter
        item_to_update = Item_location.query.get(loc_id)

        if not item_to_update:
            return jsonify({"error": f"Item with ID {loc_id} not found"}), 404

        try:
            # 3. Update fields if they are provided in the JSON body
            # If a field is missing in JSON, it keeps the current value from the DB
            item_to_update.item = data.get("item", item_to_update.item)
            item_to_update.Category = data.get("Category", item_to_update.Category)
            item_to_update.Description = data.get("Description", item_to_update.Description)
            item_to_update.Location = data.get("Location", item_to_update.Location)

            # 4. Save changes
            db.session.commit()

            # 5. Return a flat structure (No nested "data" key)
            return jsonify({
                "message": f"Successfully updated '{item_to_update.item}'",
                "Loc_id": item_to_update.Loc_id,
                "item": item_to_update.item,
                "Category": item_to_update.Category,
                "Description": item_to_update.Description,
                "Location": item_to_update.Location,
                "status": "Success"
            }), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def delete_location(loc_id):
        try:
            # 1. Find the location record by the ID from the URL
            item_to_delete = Item_location.query.get(loc_id)

            if not item_to_delete:
                return jsonify({"error": f"Item location with ID {loc_id} not found"}), 404

            # 2. Delete the record from the database
            db.session.delete(item_to_delete)
            db.session.commit()

            # 3. Return a flat JSON response
            return jsonify({
                "message": f"Successfully deleted '{item_to_delete.item}' from your location list",
                "Loc_id": loc_id,
                "status": "Success"
            }), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500