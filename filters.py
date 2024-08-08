def get_numerical_filters():
  filters = {}
  filter_options = {
      1: "price",
      2: "rating",
      3: "experience"
  }

  while True:
    try:
      filter_choice = int(input("Enter filter number (1 for price, 2 for rating, 3 for experience, 0 to exit): "))
      if filter_choice == 0:
        break
      elif filter_choice in filter_options:
        filter_type = filter_options[filter_choice]
        min_value = float(input(f"Enter minimum {filter_type}: "))
        max_value = float(input(f"Enter maximum {filter_type}: "))
        filters[filter_type] = {'$gte': min_value, '$lte': max_value}
      else:
        print("Invalid filter choice. Please try again.")
    except ValueError:
      print("Invalid input. Please enter a number.")

  return filters


