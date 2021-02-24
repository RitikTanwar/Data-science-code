#include<iostream>
using namespace std;
int main(){
    int n;
    cin>>n;
    while(1){
        if(n==42) break;
        cout<<n<<"\n";
        cin>>n;
    }
    return 0;
}