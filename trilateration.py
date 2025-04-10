import numpy as np
import matplotlib.pyplot as plt

# %% Trilatération avec aproximation arbitraire

def trilateration_2d(anchors, distances):
    if len(anchors) < 2:
        raise ValueError("Au moins 2 ancres sont nécessaires pour la trilatération 2D")
    
    A, B = anchors[0], anchors[1]
    dA, dB = distances[0], distances[1]
    
    AB = B - A
    dAB = np.linalg.norm(AB)
    
    if dAB > (dA + dB) or dAB < abs(dA - dB):
        raise ValueError("Pas de solution possible avec les distances fournies")
    
    a = (dA**2 - dB**2 + dAB**2) / (2 * dAB)
    h = np.sqrt(dA**2 - a**2)
    
    P = A + a * (AB) / dAB
    perpendicular = np.array([-AB[1], AB[0]]) / dAB
    
    solution1 = P + h * perpendicular
    solution2 = P - h * perpendicular
    
    if len(anchors) > 2:
        C = anchors[2]
        dC = distances[2]
        dist1 = abs(np.linalg.norm(solution1 - C) - dC)
        dist2 = abs(np.linalg.norm(solution2 - C) - dC)
        return solution1 if dist1 < dist2 else solution2
    
    return solution1

def plot_trilateration(anchors, distances, estimated_position):

    plt.figure(figsize=(8, 8))
    
    # Afficher les ancres
    for i, (anchor, dist) in enumerate(zip(anchors, distances)):
        plt.scatter(*anchor, color='red', s=100, label=f'Ancre {i+1}' if i == 0 else None)
        circle = plt.Circle(anchor, dist, color='blue', fill=False, alpha=0.3)
        plt.gca().add_patch(circle)
        plt.text(anchor[0], anchor[1]+0.3, f'A{i+1}', ha='center')
    
    # Afficher la position estimée
    plt.scatter(*estimated_position, color='green', s=100, label='Position estimée')
    plt.text(estimated_position[0], estimated_position[1]+0.3, 'Estimation', ha='center')
    
    # Configuration du graphique
    plt.title('Trilatération 2D')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.axis('equal')
    plt.grid(True)
    plt.legend()
    
    # Ajuster les limites pour voir tous les cercles
    all_x = [a[0] for a in anchors] + [estimated_position[0]]
    all_y = [a[1] for a in anchors] + [estimated_position[1]]
    max_dist = max(distances)
    plt.xlim(min(all_x)-max_dist-1, max(all_x)+max_dist+1)
    plt.ylim(min(all_y)-max_dist-1, max(all_y)+max_dist+1)
    
    plt.show()
    
# %% Barycentre (seuelement 3 ancres)

def barycentre(anchors, distances):
    assert(len(anchors)==3 and len(distances)==3)
    
    a0 = anchors[0] 
    a1 = anchors[1] 
    a2 = anchors[2] 
    
    d0 = distances[0]
    d1 = distances[1]
    d2 = distances[2]
    
    P0 = trilateration_2d([a0, a1, a2], [d0, d1, d2])
    P1 = trilateration_2d([a2, a0, a1], [d2, d0, d1])
    P2 = trilateration_2d([a1, a2, a0], [d1, d2, d0])
    
    return (P0 + P1 + P2) / 3

# %% MAIN

if __name__ == "__main__":
    # Positions des ancres (x, y)
    anchors = np.array([
        [2.0, 4.0],
        [5.0, 6.0],
        [3.0, 8.0]
    ])
    
    distances = np.array([3.0, 2.5, 4.0])
    
#    position = trilateration_2d(anchors, distances)
#    print(f"Position estimée: ({position[0]:.2f}, {position[1]:.2f})")
    
    position = barycentre(anchors, distances)
    plot_trilateration(anchors, distances, position)


# %% TEMPS REEL

# =============================================================================
# import random
# import numpy as np
# 
# def get_sensor_data_simulation(anchors, true_position=(2,3), noise_level=0.3):
#     """Génère des distances bruitées depuis une position simulée"""
#     return [np.linalg.norm(np.array(true_position) - np.array(anchor)) 
#             + random.uniform(-noise_level, noise_level) 
#             for anchor in anchors]
# 
# 
# 
# 
# import json
# 
# def get_sensor_data_file(filepath='sensor_data.json'):
#     with open(filepath) as f:
#         return json.load(f)['distances']
# 
# 
# 
# while True:
#     # Choisir une implémentation selon le hardware
#     distances = get_sensor_data_ultrasonic()  
#     # distances = get_sensor_data_simulation(anchors)
#     
#     position = trilateration_2d(anchors, distances)
#     print(f"Position: {position[0]:.2f}, {position[1]:.2f}")
#     time.sleep(0.1)  # 10Hz
# 
# 
# 
# =============================================================================
















