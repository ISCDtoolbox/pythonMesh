import itertools
import numpy as np

"""
MESH object =
    verts (dim 4 array, with 3 coords and 1 ref)
    tris  (dim 4 array, with 3 indices and 1 ref)
    quads (dim 5 array, with 4 indices and 1 ref)

SOL object =
    scalars (dim 1 array, with 1 scalar)
"""
class Parameters:
    def __init__(self):
        self.keywords = ["ertices", "riangles", "uadrilaterals", "olAtVertices"]
        self.done     = []
        self.found    = [False for k in self.keywords]
        self.begin    = [0 for k in self.keywords]
        self.numItems = [0 for k in self.keywords]
        self.offset   = 0
    def analyse(self, index, line):
        for k,kwd in enumerate(self.keywords):
            if self.found[k] and kwd not in self.done:
                self.numItems[k] = int(line.strip())
                self.offset += self.numItems[k]
                self.found[k] = False
                self.done.append(kwd)
                return 1
            if kwd in line and kwd not in self.done and line[0]!="#":
                self.begin[k] = index+3 if kwd=="olAtVertices" else index+2
                self.found[k] = True
    def get_infos(self, path):
        for j in range(len(self.keywords)):
            with open(path) as f:
                f.seek(0)
                for i,l in enumerate(f):
                    if i>self.offset:
                        if self.analyse(i,l):
                            break
def readMesh(path):
    params = Parameters()
    params.get_infos(path)
    verts, tris, quads = None, None, None
    print(params.numItems)
    with open(path) as f:
        X = " ".join([l for l in itertools.islice(f, params.begin[0], params.begin[0] + params.numItems[0])])
        verts = np.fromstring(X, sep=" ")
        verts = verts.reshape((params.numItems[0],4))
        if params.numItems[1]:
            f.seek(0)
            X = " ".join([l.strip() for l in itertools.islice(f, params.begin[1], params.begin[1] + params.numItems[1])])
            tris = np.fromstring(X, sep=" ",dtype=int)
            tris = tris.reshape((params.numItems[1],4))
            tris[:,:3]-=1
        else:
            tris = np.array([])
        if params.numItems[2]:
            f.seek(0)
            X = " ".join([l for l in itertools.islice(f, params.begin[2], params.begin[2] + params.numItems[2])])
            quads = np.fromstring(X, sep=" ",dtype=int).reshape((params.numItems[2],5))
            quads[:,:4]-=1
        else:
            quads = np.array([])
        return [verts, tris, quads]
    return None
def readSol(path):
    params = Parameters()
    params.get_infos(path)
    with open(path) as f:
        X = " ".join([l for l in itertools.islice(f, params.begin[3], params.begin[3] + params.numItems[3])])
        scalars = np.fromstring(X, sep=" ")
        return np.array(scalars)

def writeMesh(path, verts, tris=None, quads=None, refs=None):
    if type(verts).__module__ != np.__name__:
        verts = np.array(verts)
    if type(tris).__module__ != np.__name__:
        tris = np.array(tris)
    if type(quads).__module__ != np.__name__:
        quads = np.array(quads)
    with open(path,"w") as f:
        f.write("MeshVersionFormatted 1\nDimension 3\nVertices\n"+str(len(verts))+"\n")
        #f.write("\n".join([" ".join([x for x in l])[:-2] for l in verts.astype('|S10')]) + "\n")
        f.write("\n".join([" ".join([str(x) for x in l])[:-2] for l in verts]) + "\n")
        try:
            if tris.size:
                f.write('Triangles\n'+str(len(tris))+"\n")
                tris[:,:3]+=1
                #f.write("\n".join([" ".join([x for x in l]) for l in tris.astype('|S9')]) + "\n")
                f.write("\n".join([" ".join([str(x) for x in l]) for l in tris]) + "\n")
        except:
            pass
        try:
            if quads.size:
                f.write('Quadrilaterals\n'+str(len(quads))+"\n")
                quads[:,:4]+=1
                #f.write("\n".join([" ".join([x for x in l]) for l in tris.astype('|S9')]) + "\n")
                f.write("\n".join([" ".join([str(x) for x in l]) for l in quads]) + "\n")
        except:
            pass

def writeSol(path, sol):
    if type(sol).__module__ != np.__name__:
        sol = np.array(sol)
    with open(path,"w") as f:
        ind = "1"# if len(sol[0]) == 1 else "2"
        f.write("MeshVersionFormatted 1\nDimension 3\nSolAtVertices\n"+str(len(sol))+"\n1 " + ind + "\n")
        if ind == "1":
            #f.write("\n".join([x for x in sol.astype('|S15')]))
            f.write("\n".join(['%f' % x for x in sol]))
        elif ind == "2":
            for t in sol:
                f.write(" ".join([str(x) for x in t]) + "\n")
