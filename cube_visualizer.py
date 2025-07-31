"""
3D Rubik's Cube Visualizer
==========================
Advanced visualization module for demonstrating cube states and solving process.
Supports both static rendering and animation of solution sequences.

Author: AI Assistant
Challenge: Collins Aerospace Design Dexterity Challenge
"""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
from typing import List, Tuple
import matplotlib.animation as animation
from rubiks_cube_solver import RubiksCube

class Cube3DVisualizer:
    """
    3D visualization class for Rubik's cube using matplotlib.
    Provides static rendering and animation capabilities.
    """
    
    # Color mapping for faces
    FACE_COLORS = {
        0: '#FFFFFF',  # White
        1: '#FF0000',  # Red  
        2: '#0000FF',  # Blue
        3: '#FFA500',  # Orange
        4: '#00FF00',  # Green
        5: '#FFFF00'   # Yellow
    }
    
    def __init__(self, cube: RubiksCube):
        self.cube = cube
        self.fig = None
        self.ax = None
        
    def setup_plot(self):
        """Initialize 3D plot"""
        self.fig = plt.figure(figsize=(12, 8))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_xlim([-1.5, 1.5])
        self.ax.set_ylim([-1.5, 1.5])
        self.ax.set_zlim([-1.5, 1.5])
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        self.ax.set_title('Rubik\'s Cube - Collins Aerospace Challenge', fontsize=14, fontweight='bold')
        
    def _create_cube_face(self, center: Tuple[float, float, float], 
                          normal: Tuple[float, float, float], 
                          face_data: np.ndarray) -> List:
        """Create 3D representation of a cube face"""
        faces = []
        
        # Define face orientation vectors
        if abs(normal[0]) == 1:  # X-axis faces (Left/Right)
            u_vec = np.array([0, 1, 0])
            v_vec = np.array([0, 0, 1])
        elif abs(normal[1]) == 1:  # Y-axis faces (Front/Back)
            u_vec = np.array([1, 0, 0])
            v_vec = np.array([0, 0, 1])
        else:  # Z-axis faces (Up/Down)
            u_vec = np.array([1, 0, 0])
            v_vec = np.array([0, 1, 0])
        
        # Create 9 small squares for each face
        for i in range(3):
            for j in range(3):
                # Calculate position of small square
                offset_u = (i - 1) * 0.3 * u_vec
                offset_v = (j - 1) * 0.3 * v_vec
                square_center = np.array(center) + offset_u + offset_v
                
                # Create square vertices
                vertices = []
                for di in [-0.15, 0.15]:
                    for dj in [-0.15, 0.15]:
                        vertex = square_center + di * u_vec + dj * v_vec
                        vertices.append(vertex)
                
                # Order vertices for proper face
                square_vertices = [vertices[0], vertices[1], vertices[3], vertices[2]]
                color = self.FACE_COLORS[face_data[i][j]]
                faces.append((square_vertices, color))
        
        return faces
    
    def render_cube(self, title: str = "Rubik's Cube State"):
        """Render current cube state in 3D"""
        if self.fig is None:
            self.setup_plot()
        
        self.ax.clear()
        self.ax.set_xlim([-1.5, 1.5])
        self.ax.set_ylim([-1.5, 1.5])
        self.ax.set_zlim([-1.5, 1.5])
        self.ax.set_title(title, fontsize=14, fontweight='bold')
        
        # Define face centers and normals
        face_configs = [
            ((0, 1, 0), (0, 1, 0)),    # Front face
            ((1, 0, 0), (1, 0, 0)),    # Right face  
            ((0, 0, 1), (0, 0, 1)),    # Up face
            ((0, -1, 0), (0, -1, 0)),  # Back face
            ((-1, 0, 0), (-1, 0, 0)),  # Left face
            ((0, 0, -1), (0, 0, -1))   # Down face
        ]
        
        all_faces = []
        
        for face_idx, (center, normal) in enumerate(face_configs):
            face_squares = self._create_cube_face(center, normal, self.cube.faces[face_idx])
            all_faces.extend(face_squares)
        
        # Add all faces to plot
        for vertices, color in all_faces:
            face = Poly3DCollection([vertices], alpha=0.9, linewidth=0.5, edgecolor='black')
            face.set_facecolor(color)
            self.ax.add_collection3d(face)
        
        # Add cube edges for better definition
        self._add_cube_wireframe()
        
        plt.tight_layout()
        
    def _add_cube_wireframe(self):
        """Add wireframe edges to cube for better visibility"""
        # Define cube vertices
        vertices = [
            [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],  # Bottom face
            [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]       # Top face
        ]
        
        # Define edges
        edges = [
            [0, 1], [1, 2], [2, 3], [3, 0],  # Bottom face edges
            [4, 5], [5, 6], [6, 7], [7, 4],  # Top face edges  
            [0, 4], [1, 5], [2, 6], [3, 7]   # Vertical edges
        ]
        
        for edge in edges:
            points = np.array([vertices[edge[0]], vertices[edge[1]]])
            self.ax.plot3D(points[:, 0], points[:, 1], points[:, 2], 'k-', alpha=0.3, linewidth=0.5)
    
    def animate_solution(self, solution: List[str], save_gif: bool = False):
        """Animate the solving process"""
        if not solution:
            print("No solution to animate")
            return
        
        self.setup_plot()
        
        # Store initial state
        initial_cube = self.cube.copy()
        
        def animate_frame(frame):
            if frame == 0:
                # Reset to scrambled state
                self.cube.faces = initial_cube.faces.copy()
                title = "Scrambled State"
            else:
                # Apply next move
                move = solution[frame - 1]
                self.cube.apply_move(move)
                title = f"Move {frame}: {move}"
                
                if frame == len(solution):
                    title += " - SOLVED! ✅"
            
            self.render_cube(title)
            
        # Create animation
        frames = len(solution) + 1
        anim = animation.FuncAnimation(
            self.fig, animate_frame, frames=frames, 
            interval=1500, repeat=True, blit=False
        )
        
        if save_gif:
            anim.save('cube_solution.gif', writer='pillow', fps=0.67)
            print("Animation saved as 'cube_solution.gif'")
        
        plt.show()
        return anim
    
    def show_comparison(self, other_cube: RubiksCube):
        """Show side-by-side comparison of two cube states"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8), subplot_kw={'projection': '3d'})
        
        # Setup first cube
        self.ax = ax1
        self.render_cube("Original State")
        
        # Setup second cube  
        original_cube = self.cube
        self.cube = other_cube
        self.ax = ax2
        self.render_cube("Solved State")
        
        # Restore original
        self.cube = original_cube
        
        plt.tight_layout()
        plt.show()


class CubeNetVisualizer:
    """
    2D net visualization of cube (unfolded layout)
    Useful for detailed state analysis and presentations
    """
    
    def __init__(self, cube: RubiksCube):
        self.cube = cube
        
    def render_net(self, title: str = "Cube Net Layout"):
        """Render cube as 2D net (unfolded)"""
        fig, ax = plt.subplots(figsize=(12, 9))
        
        # Define net layout positions (face positions in grid)
        net_layout = {
            2: (1, 0),  # Up
            4: (0, 1),  # Left  
            0: (1, 1),  # Front
            1: (2, 1),  # Right
            3: (3, 1),  # Back
            5: (1, 2)   # Down
        }
        
        colors = ['white', 'red', 'blue', 'orange', 'green', 'yellow']
        
        for face_idx, (grid_x, grid_y) in net_layout.items():
            face_data = self.cube.faces[face_idx]
            
            # Draw 3x3 grid for each face
            for i in range(3):
                for j in range(3):
                    x = grid_x * 3 + j
                    y = grid_y * 3 + (2 - i)  # Flip Y for proper orientation
                    
                    color_idx = face_data[i][j]
                    rect = plt.Rectangle((x, y), 1, 1, 
                                       facecolor=colors[color_idx], 
                                       edgecolor='black', linewidth=2)
                    ax.add_patch(rect)
        
        # Add face labels
        face_labels = ['F', 'R', 'U', 'B', 'L', 'D']
        for face_idx, (grid_x, grid_y) in net_layout.items():
            x = grid_x * 3 + 1.5
            y = grid_y * 3 + 1.5
            ax.text(x, y, face_labels[face_idx], 
                   ha='center', va='center', fontsize=16, fontweight='bold')
        
        ax.set_xlim(0, 12)
        ax.set_ylim(0, 9)
        ax.set_aspect('equal')
        ax.set_title(title, fontsize=16, fontweight='bold')
        ax.set_xticks([])
        ax.set_yticks([])
        
        plt.tight_layout()
        plt.show()


def demo_visualization():
    """Demonstration of visualization capabilities"""
    print("🎨 3D Cube Visualization Demo")
    print("=" * 40)
    
    # Create and scramble cube
    cube = RubiksCube()
    original_cube = cube.copy()
    
    scramble = cube.scramble(12)
    print(f"Scramble: {' '.join(scramble)}")
    
    # Create visualizers
    viz_3d = Cube3DVisualizer(cube)
    viz_net = CubeNetVisualizer(cube)
    
    # Show scrambled state
    print("\n📊 Showing scrambled cube...")
    viz_3d.render_cube("Scrambled Cube State")
    plt.show()
    
    # Show net layout
    print("\n📋 Showing cube net layout...")
    viz_net.render_net("Scrambled Cube - Net Layout")
    
    # Show comparison
    print("\n🔄 Showing before/after comparison...")
    viz_3d.show_comparison(original_cube)
    
    print("\n✨ Visualization demo complete!")


if __name__ == "__main__":
    demo_visualization()