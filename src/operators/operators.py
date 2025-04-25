def data_join_operator(names, scores, nationalities):
    return [
        {"name": n, "score": s, "nationality": nat}
        for n, s, nat in zip(names, scores, nationalities)
    ]

def duplicate_check_operator(records):
    seen = set()
    result = []
    for record in records:
        if record["name"] not in seen:
            result.append(record)
            seen.add(record["name"])
    return result

def data_grouping_by_nationality_operator(records):

    result = {}
    for record in records:
        nationality = record["nationality"]
        if nationality not in result:
            result[nationality] = []
        result[nationality].append(record)
    return result

def average_score_calculation_operator(grouped_records):
   
    result = {}
    for nationality, records in grouped_records.items():
        total_score = sum(record["score"] for record in records)
        avg_score = total_score / len(records)
        result[nationality] = avg_score
    return result

def highest_score_retrieval_operator(grouped_records):
   
    result = {}
    for nationality, records in grouped_records.items():
        top_player = max(records, key=lambda x: x["score"])
        result[nationality] = top_player
    return result

def display_average_and_top_player_operator(avg_scores, top_players):
   
    result = []
    for nationality in avg_scores.keys():
        top_player = top_players[nationality]
        result.append({
            "nationality": nationality,
            "average_score": avg_scores[nationality],
            "top_player": f"{top_player['name']} ({top_player['score']})"
        })
    return result

def overall_best_group_and_top_three_operator(grouped_records, avg_scores):
    
   
    best_group = max(avg_scores.items(), key=lambda x: x[1])
    
    all_players = []
    for records in grouped_records.values():
        all_players.extend(records)
    
    top_three = sorted(all_players, key=lambda x: x["score"], reverse=True)[:3]
    top_three_info = [f"{p['name']} ({p['score']})" for p in top_three]
    
    return {
        "best_group": {
            "nationality": best_group[0],
            "average_score": best_group[1]
        },
        "top_three_individuals": top_three_info
    }