from sqlmodel import Session, select
from db.session import engine
# 确保导入了你要查看的模型
from models.user import User
from models.chat import ChatMessage
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def view_database():
    print("🔍 正在连接数据库...\n")
    with Session(engine) as session:

        # 1. 查看所有用户
        print("=" * 40)
        print("👤 用户表 (User)")
        print("=" * 40)
        users = session.exec(select(User)).all()
        if not users:
            print("空空如也，还没有用户~")
        for u in users:
            print(f"ID: {u.id} | 用户名: {u.username} | 邮箱: {u.email} | 角色: {u.user_role}")

        # 2. 查看所有聊天记录
        print("\n" + "=" * 40)
        print("💬 聊天记录表 (ChatMessage)")
        print("=" * 40)
        chats = session.exec(select(ChatMessage)).all()
        if not chats:
            print("还没有聊天记录，快去调戏一下大模型吧~")
        for c in chats:
            # 为了防止打印太长，限制显示前 20 个字符
            short_content = c.content[:90].replace('\n', ' ') + "..." if len(c.content) > 90 else c.content
            print(f"用户ID: {c.user_id} | 内容: {short_content}")


if __name__ == "__main__":
    view_database()

# chcp 65001
# python check_db.py