define([], function () {
	var user1 = {"firstName": "Sebastiaan"
	,"lastName": "Deckers"
	,"dateOfBirth": "09/05/1983"
	,"about": "Lorem Ipsum Rockstar"
	,"id": 1
	,"profileImage": "/dummy/user2.png"};
	
	var user2 = {"firstName": "Wolf"
	,"lastName": "Maehr"
	,"dateOfBirth": "09/05/1973"
	,"about": "UX Lorem Ipsum Rockstar"
	,"id": 2
	,"profileImage": "/dummy/user3.png"};
	
	var user3 = {"firstName": "Veron"
	,"lastName": "Boobs"
	,"dateOfBirth": "09/05/1988"
	,"about": "Lorem Ipsum Tits"
	,"id": 3
	,"profileImage": "/dummy/user1.png"};
	
	var user4 = {"firstName": "Sayanee"
	,"lastName": "Basu"
	,"dateOfBirth": "09/08/1983"
	,"about": "That's not even cleavage!"
	,"id": 4
	,"profileImage": "/dummy/user0.png"};
	
	var allUsers = [user1, user2, user3, user4];
		
	return {

	// USERS
		getAllUsers: function() {
			return allUsers;
		},

		getMyProfile: function () {
			return user1;
		},
		
		getRandomProfile: function() {
			return [allUsers[Math.floor((Math.random()*allUsers.length)+1)]];
		},
		
	// CONNECTIONS
		getFriends: function () {
			return [user2, user3];
		},
		
		getFriendsOfFriends: function () {
			return [user4];
		},
		
		getTopMatchmakers: function () {
			return [user3, user1, user4, user2];
		},

	// ACTIVITIES
		sexyTimes: [],
		recentActivity: [],


	};

});