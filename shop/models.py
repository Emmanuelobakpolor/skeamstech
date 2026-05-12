from django.db import models


class ShopTab(models.Model):
    """Represents a product tab/group (e.g., 'Automation', 'Solar & Inverters')"""
    name = models.CharField(max_length=200, unique=True)
    display_name = models.CharField(max_length=200, help_text="Display name shown on the shop page")
    description = models.CharField(max_length=500, blank=True)
    order = models.IntegerField(default=0, help_text="Display order (lower numbers appear first)")
    is_active = models.BooleanField(default=True)
    is_hardcoded = models.BooleanField(default=False, help_text="If True, this tab uses hardcoded products (Automation)")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Shop Tab'
        verbose_name_plural = 'Shop Tabs'

    def __str__(self):
        return self.display_name


class ShopCategory(models.Model):
    """Product categories within a tab"""
    tab = models.ForeignKey(
        ShopTab,
        on_delete=models.CASCADE,
        related_name='categories',
        null=True,
        blank=True
    )
    name = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['tab', 'name']
        verbose_name_plural = 'Shop Categories'

    def __str__(self):
        if self.tab:
            return f"{self.tab.display_name} - {self.name}"
        return self.name


class ShopProduct(models.Model):
    category = models.ForeignKey(
        ShopCategory,
        on_delete=models.CASCADE,
        related_name='products'
    )
    name = models.CharField(max_length=200)
    description = models.TextField()
    application = models.CharField(max_length=300, blank=True)
    image = models.ImageField(upload_to='shop_products/', blank=True, null=True)
    spec_speed = models.CharField(max_length=100, blank=True)
    spec_weight = models.CharField(max_length=100, blank=True)
    spec_voltage = models.CharField(max_length=100, blank=True)
    spec_power = models.CharField(max_length=100, blank=True)
    spec_storage = models.CharField(max_length=100, blank=True)
    spec_connectivity = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.category.name} — {self.name}"
