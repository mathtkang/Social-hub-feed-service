from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


# 숫자, 문자, 특수문자 중 2가지 이상을 포함하는지 확인
class CharacterClassesValidator:
    def validate(self, password, user=None):
        character_classes = 0
        if any(char.isdigit() for char in password):
            character_classes += 1
        if any(char.isalpha() for char in password):
            character_classes += 1
        if not character_classes >= 2:
            raise ValidationError(
                _("비밀번호에 숫자, 문자, 특수문자 중 2가지 이상을 포함해야합니다"),
                code="password_classes_not_met",
            )
        
# 3회 이상 연속되는 문자 사용을 방지
class NoConsecutiveCharactersValidator:
    def validate(self, password, user=None):
        consecutive_count = 0
        for i in range(1, len(password)):
            if ord(password[i]) == ord(password[i - 1]):
                consecutive_count += 1
                if consecutive_count >= 3:
                    raise ValidationError(
                        _("비밀번호에 2회 이상 연속 되는 문자는 사용이 불가 합니다."),
                        code="consecutive_characters",
                    )
            else:
                consecutive_count = 0