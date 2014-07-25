Feature: Accounts App :: Social login
    As a member
    I want to be able to login with my social account

    Scenario: Social login of non-logged-in user
        Given I was a visitor
        When I login using my facebook account
        Then I was asked to update my account password
        And I update my account password
        When I login using my twitter account
        Then my account was associated with both facebook and twitter
        When I login using my google account
        Then my account was associated with facebook, twitter and google

    Scenario: Social login of logged-in user
        Given I was a logged in user
        When I go to the login page
        Then I did not see the login form
        And I see the notification that I am currently login
        When I login using my facebook account
        Then my account was associated with facebook
        When I login using my twitter account
        Then my account was associated with both facebook and twitter
        When I login using my google account
        Then my account was associated with facebook, twitter and google
