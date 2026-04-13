# M151_Engine
This is a prototype of game engine M151 Engine


claude --resume 18031f62-180a-41b9-8c18-e463dd456e53


● The file is at example/entity_camera_relationship/main.py. Run it with:
                                                                                                                                                                                                                                                                                                                              
  python example/entity_camera_relationship/main.py                                                                                                                                                                                                                                                                           
                                                                                                                                                                                                                                                                                                                              
  Here's what the example teaches and how it's structured:                                                                                                                                                                                                                                                                    
                                                            
  ---                                                                                                                                                                                                                                                                                                                         
  What's in it                                                                                                                                                                                                                                                                                                                
              
  Three coordinate spaces, explained with worked numbers:
  - World space — where the entity truly lives on the 4113×1598 map                                                                                                                                                                                                                                                           
  - Camera space — the rectangle of world the screen is showing (tracked by cam_x, cam_y)                                                                                                                                                                                                                                     
  - Screen space — derived: screen_x = world_x - cam_x                                                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                                                                                                              
  Entity class — owns world_x / world_y only. It has no awareness of the camera. The comment on draw() explicitly explains why it accepts screen coordinates from outside rather than computing them itself.
                                                                                                                                                                                                                                                                                                                              
  Camera class — two core methods:                          
  - follow() — a two-step algorithm: aim for the entity's center, then clamp to map bounds. Both steps are explained with the algebra so you can verify why the formula works.                                                                                                                                                
  - world_to_screen() — the one-line formula with an intuition explanation and a concrete worked example.                                                                                                                                                                                                                     
  - draw_map() — explains the area= optimization vs the naive full-blit alternative.                     
                                                                                                                                                                                                                                                                                                                              
  read_keys() — the diagonal normalization (0.707 / 1/√2) is explained with the magnitude math, building on the note already in your KeyboardController docstring.                                                                                                                                                            
                                                                                                                                                                                                                                                                                                                              
  Debug HUD — shows all three coordinate spaces live while you move. The key thing to observe: screen_x/screen_y stay near (480, 270) as you walk across the map — except when the camera hits a map edge and the entity slides toward the corner.
