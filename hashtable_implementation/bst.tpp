/* TODO: Implement the functions for the class BST */
/* Write your code below */
template <typename K, typename V>
vector<V> BST<K, V>::getInorder(Node* node) const
{
    vector<V> x;
    if (node==nullptr)
    {
        return x;
    }
    vector<V> left=getInorder(node->left);
    x.insert(x.end(),left.begin(),left.end());
    x.push_back(node->value);
    vector<V> right = getInorder(node->right);
    x.insert(x.end(),right.begin(),right.end());
    return x;
}
template <typename K, typename V>
vector<V> BST<K, V>::getInorderWithUpperBound(Node* node, const K& upper_bound) const
{
    vector<V> x;
    if (node==nullptr)
    {
        return x;
    }
    vector<V> left=getInorderWithUpperBound(node->left,upper_bound);
    if (node->key<upper_bound)
    {
        x.insert(x.end(),left.begin(),left.end());
        x.push_back(node->value);
        vector<V> right=getInorderWithUpperBound(node->right,upper_bound);
        x.insert(x.end(),right.begin(),right.end());
    }
    else
    {
        x=left;
    }
    return x; 

}
template <typename K, typename V>
vector<V> BST<K, V>::getInorderWithLowerBound(Node* node, const K& lower_bound) const
{
    vector<V> x;
    if (node==nullptr)
    {
        return x;
    }
    vector<V> left=getInorderWithLowerBound(node->left,lower_bound);
    if (node->key>lower_bound)
    {
        x.insert(x.end(),left.begin(),left.end());
        x.push_back(node->value);
        vector<V> right=getInorderWithLowerBound(node->right,lower_bound);
        x.insert(x.end(),right.begin(),right.end());
    }
    else
    {
        x=left;
    }
    return x; 

}