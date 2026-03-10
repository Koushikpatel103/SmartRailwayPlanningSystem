def recommend_coaches(predicted_passengers, capacity):

    seats_per_coach = 72

    if predicted_passengers > capacity:

        extra = predicted_passengers - capacity
        coaches = (extra // seats_per_coach) + 1

        return coaches

    return 0