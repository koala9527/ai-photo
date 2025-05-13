from app.models import WechatCode
from config.database import get_db

class CodeService:
    @staticmethod
    def validate_code(activation_code: str) -> tuple[bool, str, WechatCode]:
        """
        验证激活码
        返回: (是否有效, 错误信息, 激活码记录)
        """
        with get_db() as db:
            code_record = db.query(WechatCode).filter(WechatCode.code == activation_code).first()
            
            if not code_record:
                return False, '激活码不存在', None
            
            if code_record.status == 1:
                return False, '激活码已被使用', None
            
            if code_record.status == 2:
                return False, '激活码正在使用中', None
            
            return True, '', code_record

    @staticmethod
    def mark_code_as_using(code_record: WechatCode) -> None:
        """将激活码标记为使用中"""
        with get_db() as db:
            code_record.status = 2
            db.add(code_record)

    @staticmethod
    def mark_code_as_used(code_record: WechatCode) -> None:
        """将激活码标记为已使用"""
        with get_db() as db:
            code_record.status = 1
            db.add(code_record)

    @staticmethod
    def reset_code_status(code_record: WechatCode) -> None:
        """重置激活码状态"""
        with get_db() as db:
            code_record.status = 0
            db.add(code_record) 