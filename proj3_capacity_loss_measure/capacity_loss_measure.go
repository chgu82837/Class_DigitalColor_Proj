package main

import (
    "fmt"
    // "time"
    "math"
)

func main() {
    H,V := 512,512
    var n int
    max,max_k,max_L,tmp := 0.0,0,0.0,0.0
    fmt.Printf("Please input n:")
    fmt.Scanf("%d\n", &n)
    fmt.Printf("Please input H:")
    fmt.Scanf("%d\n", &H)
    fmt.Printf("Please inputn V:")
    fmt.Scanf("%d\n", &V)


    // Log2 testing
    // fmt.Printf("%f,",math.Log2(float64(2 * n + 1)))
    // fmt.Printf("%f,",math.Log2(4.0))
    // fmt.Printf("%f,",math.Log2(8.0))
    // fmt.Printf("%f\n",math.Log2(5.0))

    K := 1
    L := math.Floor(math.Log2(float64(2 * n + 1)))

    fmt.Println("Calculating ...")
    fmt.Println(" n   | K   | L   | max_k | max     | result")
    for L <= 64.0 {
        tmp = math.Floor(math.Floor(float64(H * V / n)) / float64(K)) * L
        if tmp > max {
            max_k = K
            max_L = L
            max = tmp
        }
        fmt.Printf(" %-3d | %-3d | %-3.0f | %-5d | %-7.0f | %-.0f\n",n,K,L,max_k,max,tmp)
        K++
        L = math.Floor(float64(K) * math.Log2(float64(2 * n + 1)))
    }

    OPT := math.Log2(float64(2 * n + 1)) * math.Floor(float64(H * V / n))
    fmt.Printf("MXC is %.0f, max_k: %d, max_L: %.0f, OPT: %f, CL: %f %%\n",max,max_k,max_L,OPT,(1.0 - float64(max) / OPT) * 100.0)
}
