// Tries to recruit philosophers if possible, otherwise bets for apollo.

#include <bits/stdc++.h>

using namespace std;

string met[2][2] ={{"3 3", "9 10"},
{"5 3", "6 7"}}; // location of islands

void wait_for_turn()
{
    string info;
    while(info!="-4") // waits for its turn
        cin>>info;
    cin>>info;
}

int main()
{
    int player_num, met_num=0;
    cin>>player_num;
    while(1)
    {
        string info;
        cin>>info;
        bool atbet = 1;
        wait_for_turn();
        cout<<"l at 1"<<endl;
        cin>>info;
        if(info == "-3") // incorrect move
        {
            wait_for_turn();
            cout<<"l at 2"<<endl;
            cin>>info;
            if(info == "-3")
            {
                wait_for_turn();
                cout<<"l ap 1"<<endl;
                atbet=0;
                break;
            }
        }
        wait_for_turn();
        cout<<"l at 1"<<endl;
        cin>>info;
        if(info == "-3") // incorrect move
        {
            wait_for_turn();
            cout<<"l ap 1"<<endl;
            atbet=0;
        }
        while(atbet)
        {
            wait_for_turn();
            cout<<"r"<<endl;
            cin>>info;
            if(info=="-3")
            {
                atbet=0;
            }
            else if(info=="-7")
            {
                wait_for_turn();
                cout<<met[player_num][met_num++]<<endl;
            }
        }
        cout<<"p"<<endl;
    }
}