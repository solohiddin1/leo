from django.test import TestCase

from apps.product.models import Category, Product, SubCategory
from apps.shared.utils.result_codes import ResultCodes
from apps.transaction.models import Bonus, BonusCode, UserSumma
from apps.transaction.services.bonus_service import BonusService
from apps.user.models import User


class BonusTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Nasoslar")
        self.subcategory = SubCategory.objects.create(name="Suv nasoslari", category=self.category)
        self.product = Product.objects.create(
            name="Test Product 100",
            price=1500000,
            category=self.subcategory,
        )
        self.user = User.objects.create_user(
            username="998901234567",
            telegram_id="12345678",
            first_name="Ali",
            is_verified=True,
        )

    def test_bonus_creation_generates_codes_with_is_active(self):
        bonus = Bonus.objects.create(
            product=self.product,
            summa=50000,
            prefix="WQ15A0000",
            quantity=100,  # small quantity for speed in test
            is_active=True,
        )
        self.assertTrue(bonus.is_active)
        self.assertEqual(bonus.codes.count(), 100)

        # First code should be WQ15A0000
        first_code = bonus.codes.first()
        self.assertEqual(first_code.code, "WQ15A0000")
        self.assertFalse(first_code.is_used)

    def test_inactive_bonus_returns_not_found(self):
        bonus = Bonus.objects.create(
            product=self.product,
            summa=50000,
            prefix="TST1A0000",
            quantity=10,
            is_active=False,
        )
        code = bonus.codes.first().code

        # check_code should return BONUS_CODE_NOT_FOUND
        res = BonusService.check_code(code)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.data.get("error", {}).get("code"), ResultCodes.BONUS_CODE_NOT_FOUND.value)

        # redeem_bonus should return BONUS_CODE_NOT_FOUND
        res_redeem = BonusService.redeem_bonus(self.user, code, images=["1.jpg", "2.jpg", "3.jpg"])
        self.assertEqual(res_redeem.status_code, 400)
        self.assertEqual(res_redeem.data.get("error", {}).get("code"), ResultCodes.BONUS_CODE_NOT_FOUND.value)

        # redeem_bonus_external should return BONUS_CODE_NOT_FOUND
        res_ext = BonusService.redeem_bonus_external(self.user, code)
        self.assertEqual(res_ext.status_code, 400)
        self.assertEqual(res_ext.data.get("error", {}).get("code"), ResultCodes.BONUS_CODE_NOT_FOUND.value)

    def test_active_bonus_redeem_success_and_prevents_duplicate(self):
        bonus = Bonus.objects.create(
            product=self.product,
            summa=50000,
            prefix="ACT1A0000",
            quantity=10,
            is_active=True,
        )
        code = bonus.codes.first().code

        # Check code succeeds
        res_check = BonusService.check_code(code)
        self.assertEqual(res_check.status_code, 200)
        self.assertEqual(res_check.data.get("result", {}).get("summa"), 50000)

        # External redeem succeeds
        res_redeem = BonusService.redeem_bonus_external(self.user, code)
        self.assertEqual(res_redeem.status_code, 200)
        self.assertEqual(res_redeem.data.get("result", {}).get("awarded"), 50000)

        # Second attempt must return ALREADY_USED
        res_again = BonusService.redeem_bonus_external(self.user, code)
        self.assertEqual(res_again.status_code, 400)
        self.assertEqual(res_again.data.get("error", {}).get("code"), ResultCodes.BONUS_CODE_ALREADY_USED.value)
