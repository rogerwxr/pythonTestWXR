from flask import Flask, request, jsonify


app = Flask(__name__)


# 模拟数据库
items = []


# 获取所有或创建 (GET / POST)
@app.route('/items', methods=['GET', 'POST'])
def handle_items():
    if request.method == 'GET':
        return jsonify(items), 200
    
    # POST: 创建新项
    data = request.get_json()
    if not data:
        return jsonify({"error": "无效的数据"}), 400
        
    new_item = {
        "id": len(items) + 1,
        "name": data.get('name'),
        "description": data.get('description')
    }
    items.append(new_item)
    return jsonify(new_item), 201


# 获取、更新、删除单个 (GET / PUT / DELETE)
@app.route('/items/<int:item_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_item(item_id):
    # 查找物品
    item = next((i for i in items if i['id'] == item_id), None)
    
    if not item:
        return jsonify({"error": "未找到"}), 404


    if request.method == 'GET':
        return jsonify(item), 200
    
    elif request.method == 'PUT':
        data = request.get_json()
        item['name'] = data.get('name', item['name'])
        item['description'] = data.get('description', item['description'])
        return jsonify(item), 200
    
    elif request.method == 'DELETE':
        items.remove(item)
        return '', 204


if __name__ == '__main__':
    app.run(debug=True)
