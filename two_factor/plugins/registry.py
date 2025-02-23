from django.utils.translation import gettext_lazy as _


class MethodBase:
    code = None
    verbose_name = None
    form_path = None

    def recognize_device(self, device):
        """
        Return True if the device can be handled by this method.
        """
        return False

    def get_setup_forms(self):
        """
        Return a dict where keys are setup wizard step names, and the values
        the form class matching the step.
        """
        return {}  # pragma: no cover

    def get_device_from_setup_data(self, request, setup_data):
        """
        Obtain device instance from 2fa setup wizard data.
        """
        return None  # pragma: no cover

    def get_token_form_class(self):
        """
        Return the authentication token form class.
        """
        from two_factor.forms import AuthenticationTokenForm

        return AuthenticationTokenForm


class GeneratorMethod(MethodBase):
    code = 'generator'
    verbose_name = _('Token generator')
    form_path = 'two_factor.forms.TOTPDeviceForm'

    def get_setup_forms(self):
        from two_factor.forms import TOTPDeviceForm

        return {'generator': TOTPDeviceForm}


class MethodRegistry:
    _methods = []

    def __init__(self):
        self.register(GeneratorMethod())

    def register(self, method):
        self._methods.append(method)

    def unregister(self, code):
        self._methods = [m for m in self._methods if m.code != code]

    def get_method(self, code):
        try:
            return [meth for meth in self._methods if meth.code == code][0]
        except IndexError:
            return None

    def get_methods(self):
        return self._methods

    def method_from_device(self, device):
        for method in self._methods:
            if method.recognize_device(device):
                return method
        # Default to GeneratorMethod
        return GeneratorMethod()


registry = MethodRegistry()
