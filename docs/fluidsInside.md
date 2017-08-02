# Fluid outside an object

## 1 - Preparation in Blender

### HR mesh
Here, my HR mesh will also be my LR mesh as it is a quite light example.
![alt text](https://user-images.githubusercontent.com/11873158/28872307-e808793e-7788-11e7-8198-67ab97c26638.png)

### Edit mode
![alt text](https://user-images.githubusercontent.com/11873158/28872306-e8087308-7788-11e7-9c64-1a8d5f943ecb.png)

### View in Medit after export
```bash
medit mechanical.mesh
```
![](https://user-images.githubusercontent.com/11873158/28872310-e8208d12-7788-11e7-8924-14db939ecde5.png)

### Tetrahedral mesh
```bash
tetgen -pgaA mechanical.mesh
```
![alt text](https://user-images.githubusercontent.com/11873158/28872309-e80db05c-7788-11e7-97f1-928eac24f13a.png)

### Volume remeshing
```bash
mmg3d mechanical.1.mesh
```
![](https://user-images.githubusercontent.com/11873158/28872308-e80c7f3e-7788-11e7-93d9-d0e67d92d4a6.png)
