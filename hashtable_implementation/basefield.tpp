/* TODO: Implement the functions for the subclasses of BaseField */
template <typename T>
void PrimitiveField<T>::handleAddEntryToIndexTree(BaseBST* index_tree, Entry* entry) const
{
    BST <T,HashTable<Entry*>>* tree=dynamic_cast<BST<T,HashTable<Entry*>>*>(index_tree);
    if (!tree)
    {
        return;
    }
    T key= this->value;
    HashTable<Entry*>* entries=tree->get(key);
    if (entries)
    {
        entries->insert(entry);


    }
    else
    {
        HashTable<Entry*> new_entry;
        new_entry.insert(entry);
        tree->insert(key,new_entry);
    }
}
template <typename T>
void ListField<T>::handleAddEntryToIndexTree(BaseBST* index_tree, Entry* entry) const
{
    BST <T,HashTable<Entry*>>* tree=dynamic_cast<BST<T,HashTable<Entry*>>*>(index_tree);
    if (!tree)
    {
        return;
    }
    for (const T&item:values)
    {
        HashTable<Entry*>* entries=tree->get(item);
        if (entries)
    {
        entries->insert(entry);
    }
    else
    {
        HashTable<Entry*> new_entry;
        new_entry.insert(entry);
        tree->insert(item,new_entry);
    }

    }



}
/* Write your code below */