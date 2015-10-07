def distance2(a,b):
    return sum([(a[x]-b[x])**2 for x in range(2)])
def kmeans(examples, centers):
    maxIters = 100
    for counter in xrange(maxIters):
        square_loss = 0
        new_assignment = []
        for i, k in enumerate(examples):
            dist_all = [distance2(k, c) for c in centers]
            print "distance^2 of [" + str(k[0]) + "," + str(k[1]) + "] to each centers", dist_all
            min_idx, min_dist2 = min(enumerate(dist_all), key = lambda p: p[1])
            print "assigning to center  " + str(min_idx)
            new_assignment.append(min_idx)
            square_loss = square_loss + min_dist2
        # update step
        new_centers = []
        # TODO possible to have empty point sets?
        for c, center in enumerate(centers):
            centered_points = [examples[ex] for ex, cen in enumerate(new_assignment) if cen == c]
            
            sumDistance = [sum([a[m] for a in centered_points]) for m in range(2)]
            #sumDistance = sumByKey(centered_points)
            new_centers.append([(v/float(len(centered_points))) for v in sumDistance])
            print "moving center from " + ptostring(center) + " to " + ptostring(new_centers[-1])
            #print centered_points
        centers = new_centers
        assignment = new_assignment
        print "iteration " + str(counter) + " with loss " + str(square_loss)
        #print "center", centers
        print "assignment", assignment
        if ( counter > 0 and square_loss / last_square_loss > 0.99 ):
            break
        else:
            last_square_loss = square_loss
    return


def ptostring(k):
    return "[" + str(k[0]) + "," + str(k[1]) + "]"

points = [ [1,0],[2,1],[0,0],[0,2]]
kmeans(points, [[0,-1],[2,2]])
kmeans(points, [[-1,0],[2,0]])
