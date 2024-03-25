from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete


# @receiver(post_save)
# def update_talent_index(sender, **kwargs):
#     """
#     Update talent document when model is updated
#
#     :param sender:
#     :param kwargs:
#     :return:
#     """
#     app_label = sender._meta.app_label
#     model_label = sender._meta.model_label
#     instance = kwargs['instance']
#
#     if app_label == 'talents':
#         if model_label == 'talent':
