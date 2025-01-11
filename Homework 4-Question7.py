import numpy as np
import Homework_4_Question_6 as q6

def vector_lenght(v):
    return np.linalg.norm(v)


def super_simple_separable():

    X = np.array([[2, 3, 9, 12],
                  [5, 2, 6, 5]])
    
    y = np.array([[1, -1, 1, -1]])

    return X, y

def separable_medium():

    X = np.array([[2, -1, 1, 1],
                  [-2, 2, 2, -1]])
    
    y = np.array([[1, -1, 1, -1]])

    return X, y

def hinge(v):
    return np.where(v < 1, 1-v, 0)

# x is dxn, y is 1xn, th is dx1, th0 is 1x1
def hinge_loss(x, y, th, th0):
    v = y * (th.T@x + th0)
    return hinge(v)

# x is dxn, y is 1xn, th is dx1, th0 is 1x1, lam is a scalar
def svm_obj(x, y, th, th0, lam):

    (rows, columns)= x.shape
    average_loss = (np.sum(hinge_loss(x, y, th, th0)) / columns)
    return average_loss + lam*((vector_lenght(th))**2)


def package_ans(gd_vals):
    x, fs, xs = gd_vals
    return [x.tolist(), [fs[0], fs[-1]], [xs[0].tolist(), xs[-1].tolist()]]
    


sep_e_separator = np.array([[-0.40338351], [1.1849563]]), np.array([[-2.26910091]])

sep_m_separator = np.array([[ 2.69231855], [ 0.67624906]]), np.array([[-3.02402521]])

'''
# Test case 1
x_1, y_1 = super_simple_separable()
th1, th1_0 = sep_e_separator
ans = svm_obj(x_1, y_1, th1, th1_0, .1)
print('Test Case 1: ', ans)
# Test case 2
ans = svm_obj(x_1, y_1, th1, th1_0, 0.0)
print('Test Case 2: ', ans)

'''

# Returns the gradient of hinge(v) with respect to v.
def d_hinge(v):
    return np.where(v < 1, -1, 0)

# Returns the gradient of hinge_loss(x, y, th, th0) with respect to th
def d_hinge_loss_th(x, y, th, th0):
    v = y * (th.T@x + th0)
    return np.where(v < 1, (y*x), 0)

# Returns the gradient of hinge_loss(x, y, th, th0) with respect to th0
def d_hinge_loss_th0(x, y, th, th0):
    v = y * (th.T@x + th0)
    return np.where(v < 1, -1*y, 0)

# Returns the gradient of svm_obj(x, y, th, th0) with respect to th
def d_svm_obj_th(x, y, th, th0, lam):
    (rows, columns)= x.shape
    average_loss = (np.sum(d_hinge_loss_th(x, y, th, th0)) / columns)
    return average_loss + (2* (lam * th))

# Returns the gradient of svm_obj(x, y, th, th0) with respect to th0
def d_svm_obj_th0(x, y, th, th0, lam):
    (rows, columns)= x.shape
    average_loss = (np.sum(d_hinge_loss_th0(x, y, th, th0)) / columns)
    return np.array([[average_loss]])

# Returns the full gradient as a single vector (which includes both th, th0)
def svm_obj_grad(x, y, th, th0, lam):
    return np.vstack((d_svm_obj_th(x, y, th, th0, lam),d_svm_obj_th0(x, y, th, th0, lam)))



def gd(f, df, x0, step_size_fn, max_iter):

    temp_x = x0
    fs = []
    xs = []
    for i in range(max_iter): 

        fs.append(f(temp_x))
        xs.append(temp_x)
        step_size = step_size_fn(i) if callable(step_size_fn) else step_size_fn
        x =  temp_x - step_size * df(temp_x)
        temp_x = x

    return x, fs, xs


def batch_svm_min(data, labels, lam):

    def svm_min_step_size_fn(i):
        return 2/(i+1)**0.5
    
    init = np.zeros((data.shape[0] + 1, 1))

    def f(th):
      return svm_obj(data, labels, th[:-1, :], th[-1:,:], lam)

    def df(th):
      return svm_obj_grad(data, labels, th[:-1, :], th[-1:,:], lam)

    x, fs, xs = gd(f, df, init, svm_min_step_size_fn, 10)

    return x, fs, xs
x_1, y_1 = separable_medium()
ans = package_ans(batch_svm_min(x_1, y_1, 0.0001))
print('Test Case 1 batch_svm_min: ', ans)





'''

X1 = np.array([[1, 2, 3, 9, 10]])
y1 = np.array([[1, 1, 1, -1, -1]])
th1, th10 = np.array([[-0.31202807]]), np.array([[1.834     ]])

X2 = np.array([[2, 3, 9, 12],
               [5, 2, 6, 5]])

y2 = np.array([[1, -1, 1, -1]])

th2, th20=np.array([[ -3.,  15.]]).T, np.array([[ 2.]])



print(d_hinge_loss_th(X2[:,0:1], y2[:,0:1], th2, th20).tolist())

print(d_hinge_loss_th0(X2, y2, th2, th20).tolist())

ans=d_svm_obj_th(X2, y2, th2, th20, 0.01).tolist()

print('d_smv_obj_th test: ', ans)
'''