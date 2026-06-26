Feature: Broadcast notifications
  As a platform user
  I want updates to notify everyone
  So all users stay informed

  Scenario: Manager action creates notifications for all users
    Given a manager user "bdd_manager" and a normal user "bdd_viewer"
    And a destination named "Agadir"
    When I login as "bdd_manager" with password "secure-pass-123"
    And I create a package titled "Agadir Escape"
    Then the package "Agadir Escape" should exist
    And user "bdd_manager" should have 1 notification
    And user "bdd_viewer" should have 1 notification
    And notification for "bdd_viewer" should mention "Updated by bdd_manager (@bdd_manager)."
