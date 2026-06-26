Feature: Saved profile quick login
  As a returning user
  I want to login from saved profiles
  So I don't retype my password every time

  Scenario: Quick login from saved profile token
    Given a user "bdd_agent" with password "secure-pass-123"
    When I login as "bdd_agent" with password "secure-pass-123"
    And I logout from my account
    And I login using the first saved profile token
    Then I should be authenticated as "bdd_agent"
