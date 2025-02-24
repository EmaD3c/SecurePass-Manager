from app.models.user import User
from app.services.user_repository import UserRepository



class Facade:
    """Represent a facade."""

    _instance = None

    def __new__(cls, *args, **kwargs):
        """Override __new__ to control instance creation (Singleton)."""
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        """Initiliaze a instance of class HBnBFacade."""
        self.user_repo = UserRepository()

    # ----------------------------------------------------------- #
    ##########################_USER_###############################
    # ----------------------------------------------------------- #
    def create_user(self, user_data):
        """Create an user."""
        user = User(**user_data)
        user.hash_password(user_data["password"])
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Retrieve user's data."""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Retrieve user by mail."""
        return self.user_repo.get_user_by_email(email)

    def get_all_users(self):
        """Retrieve all users."""
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """Update the user's data."""
        user = self.user_repo.get(user_id)
        if user is None:
            return None

        # Rehash user's password and store it in data to update
        user.hash_password(user_data.get("password", user.password))
        user_data["password"] = user.password

        self.user_repo.update(user_id, user_data)
        return user

    def delete_user(self, user_id):
        """Delete user."""
        self.user_repo.delete(user_id)

        if self.user_repo.get(user_id) is None:
            return True

        return False

    # ----------------------------------------------------------- #
    ##########################_PLACE_##############################
    # ----------------------------------------------------------- #

    def create_place(self, place_data):
        """Create place."""
        owner = self.get_user(place_data["owner_id"])
        if not owner:
            raise Exception("Owner not found")

        place = Place(
            title=place_data["title"],
            price=place_data["price"],
            latitude=place_data["latitude"],
            longitude=place_data["longitude"],
            description=place_data.get("description"),
            owner_id=place_data["owner_id"],
        )
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """Retrieve place's data."""
        place = self.place_repo.get(place_id)
        if not place:
            return None

        # List of place's amenities
        # amenities = []
        # Get amenities IDs then data
        # for tup in self.association_repo.get_all():
        #    if tup.association[0] == place_id:
        #        amenities.append(self.amenity_repo.get(tup.association[1]))

        # place.amenities = amenities

        return place

    def get_all_places(self):
        """Retrieve all places."""
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """Update the place's data."""
        place = self.place_repo.get(place_id)
        if place is None:
            return None

        owner_id = self.get_user(place_data.get("owner_id", place.owner.uuid))
        if not owner_id:
            raise Exception("Owner not found")

        # No update for this attributes
        place_data["latitude"] = place.latitude
        place_data["longitude"] = place.longitude
        place_data["owner"] = place.owner

        self.place_repo.update(place_id, place_data)
        return place

    # def add_amenities(self, place_id, amenity_id):
    #    """Add amenity for the place."""

    def delete_place(self, place_id):
        """Delete a place."""
        self.place_repo.delete(place_id)

        if self.place_repo.get(place_id) is None:
            return True

        return False

    # ----------------------------------------------------------- #
    #########################_AMENITY_#############################
    # ----------------------------------------------------------- #

    def create_amenity(self, amenity_data):
        """Create an amenity."""
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Retrieve the amenity's detail."""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Retrieve all amenities."""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Update the amenity."""
        amenity = self.amenity_repo.get(amenity_id)
        if amenity is None:
            return None

        self.amenity_repo.update(amenity_id, amenity_data)
        return self.amenity_repo.get(amenity_id)

    # ----------------------------------------------------------- #
    #########################_REVIEW_##############################
    # ----------------------------------------------------------- #

    def create_review(self, review_data):
        """Create an review."""
        user = self.get_user(review_data["user_id"])
        if not user:
            raise Exception("User not found")

        place = self.get_place(review_data["place_id"])
        if not place:
            raise Exception("Place not found")

        review = Review(
            text=review_data["text"],
            rating=review_data["rating"],
            user_id=review_data["user_id"],
            place_id=review_data["place_id"],
        )

        self.review_repo.add(review)

        # user.reviews.append(review)
        # self.user_repo.update(user, user.__dict__)

        # place.reviews.append(review)
        # self.place_repo.update(place, place.__dict__)

        return review

    def get_all_reviews(self):
        """Retrieve all review's data."""
        return self.review_repo.get_all()

    def get_review(self, review_id):
        """Retrieve review's data."""
        return self.review_repo.get(review_id)

    def update_review(self, review_id, review_data):
        """Update the review."""
        review = self.review_repo.get(review_id)
        if review is None:
            return None

        self.review_repo.update(review_id, review_data)
        return review

    def delete_review(self, review_id):
        """Update the review."""
        review = self.review_repo.get(review_id)
        if review is None:
            return None

        self.review_repo.delete(review_id)
        return review_id

    # ----------------------------------------------------------- #
    #######################_PLACE_AMENITY_#########################
    # ----------------------------------------------------------- #

    def associate_place_to_amenity(self, place_id, amenity_id):
        """Associate a place and an amenity."""
        association = PlaceAmenity(place_id=place_id, amenity_id=amenity_id)

        association_list = self.place_amenity_repo.get_all()
        for tup in association_list:
            if (
                association.place_id == tup.place_id
                and association.amenity_id == tup.amenity_id
            ):
                raise Exception("This place already has that amenity.")

        self.place_amenity_repo.add(association)