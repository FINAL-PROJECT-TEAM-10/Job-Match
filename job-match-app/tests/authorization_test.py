import unittest

from unittest.mock import Mock, patch


class AuthorizationServices_Should(unittest.TestCase):
    def test_verifyPasswordTextPasswordMatchesHash(self):
        pass

    def test_getPassWordHash_GeneratesHash(self):
        pass

    def test_getPassByUsernameAdminReturnsString(self):
        pass

    def test_getPassByUsernameSeekerReturnsString(self):
        pass

    def test_getPassByUsernameCompanyReturnsString(self):
        pass

    def test_authenticateAdminReturnsAdmin(self):
        pass

    def test_authenticateAdminUsesVerifyPassword(self):
        pass

    def test_authenticateSeekerReturnsSeeker(self):
        pass

    def test_authenticateSeekerUsesVerifyPassword(self):
        pass

    def test_authenticateCompanyReturnsCompany(self):
        pass

    def test_authenticateCompanyUsesVerifyPassword(self):
        pass

    def test_createAccessTokenCreatesDecodableToken(self):
        pass

    def test_createActivationTokenCreatesDecodableToken(self):
        pass

    def test_AccessTokensAndActivationTokensCannotBeUsedInterchangeably(self):
        pass

    def test_isAuthenticatedReturnsMeaningfulToken(self):
        pass

    def test_isAuthenticatedCustomReturnsMeaningfulToken(self):
        pass

    def test_passwordChangerUpdatesCorrectTable(self):
        pass

    def test_isPasswordIdenticalByTypeVerifiesAdminPasswords(self):
        pass

    def test_isPasswordIdenticalByTypeVerifiesSeekerPasswords(self):
        pass

    def test_isPasswordIdenticalByTypeVerifiesCompanyPasswords(self):
        pass

    def test_generatePasswordGeneratesDifferentPasswords(self):
        pass

    def test_generatePassword_GeneratedPasswordHasLowerUpperNumbersSpecialChars(self):
        pass

    def test_activationTokenExistsReturnsTrueIfToken(self):
        pass

    def test_activationTokenExistsReturnsTrueIfNotFound(self):
        pass

    # Consider if below is needed
    def test_storeActivationTokenUsesInsertQuery(self):
        pass

    def test_deleteActivationTokenUsesUpdateQuery(self):
        pass
